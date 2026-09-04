#!/usr/bin/env python3
"""
Chroma-key the two green-screen jar clips, concatenate them and export an
alpha WebP frame sequence (+ manifest) for the scroll-scrubbed hero.

usage: python3 .claude/build-frames.py fall.mp4 pour.mp4
"""
import json, os, subprocess, sys, tempfile, glob
from PIL import Image

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT    = os.path.join(ROOT, 'assets', 'frames')
WIDTH  = 660           # output width  (3:4 -> 660x880)
QUAL   = 82
FPS    = 24

def key(src, dst, color, sim, blend):
    vf = (f"chromakey=0x{color}:{sim}:{blend},"
          f"despill=type=green:mix=0.6:expand=0.3,"
          f"format=rgba,scale={WIDTH}:-2:flags=lanczos")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', vf,
                    '-r', str(FPS), '-pix_fmt', 'rgba', dst], check=True)

def sample_key(src):
    """average colour of the four corners of the first frame -> hex"""
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'f.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-frames:v', '1', p], check=True)
        im = Image.open(p).convert('RGB'); w, h = im.size
        pts = [(8, 8), (w-8, 8), (8, h-8), (w-8, h-8), (w//2, 8)]
        rgb = [im.getpixel(q) for q in pts]
        avg = tuple(sum(c[i] for c in rgb)//len(rgb) for i in range(3))
        return '%02X%02X%02X' % avg

def main(fall, pour):
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, '*.webp')): os.remove(f)
    with tempfile.TemporaryDirectory() as d:
        seqs = []
        for i, src in enumerate([fall, pour]):
            col = sample_key(src)
            print('key colour', src, col)
            pat = os.path.join(d, f'c{i}_%04d.png')
            key(src, pat, col, 0.20, 0.10)
            seqs.append(sorted(glob.glob(os.path.join(d, f'c{i}_*.png'))))
        # drop the last frame of clip A (duplicate of clip B's first frame)
        frames = seqs[0][:-1] + seqs[1]
        n = 0
        for p in frames:
            im = Image.open(p).convert('RGBA')
            # kill residual green fringe: pixels that are still greenish get alpha reduced
            im.save(os.path.join(OUT, f'{n:04d}.webp'), 'WEBP', quality=QUAL, method=4)
            n += 1
        w, h = Image.open(frames[0]).size
        json.dump({'count': n, 'width': w, 'height': h, 'fps': FPS,
                   'split': len(seqs[0]) - 1},
                  open(os.path.join(OUT, 'manifest.json'), 'w'))
        size = sum(os.path.getsize(f) for f in glob.glob(os.path.join(OUT, '*.webp')))
        print(f'{n} frames, {w}x{h}, {size/1e6:.1f} MB')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
