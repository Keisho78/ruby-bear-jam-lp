const http=require('http'),fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.jpg':'image/jpeg','.png':'image/png','.mp4':'video/mp4','.svg':'image/svg+xml','.webp':'image/webp'};
http.createServer((req,res)=>{
  let p=decodeURIComponent(req.url.split('?')[0]); if(p.endsWith('/'))p+='index.html';
  const f=path.join(root,p);
  fs.stat(f,(e,st)=>{
    if(e||!st.isFile()){res.writeHead(404);return res.end('404');}
    const type=types[path.extname(f)]||'application/octet-stream';
    const range=req.headers.range;
    if(range){
      const [s,en]=range.replace('bytes=','').split('-');const start=+s,end=en?+en:st.size-1;
      res.writeHead(206,{'Content-Range':`bytes ${start}-${end}/${st.size}`,'Accept-Ranges':'bytes','Content-Length':end-start+1,'Content-Type':type});
      return fs.createReadStream(f,{start,end}).pipe(res);
    }
    res.writeHead(200,{'Content-Type':type,'Content-Length':st.size,'Accept-Ranges':'bytes','Cache-Control':'no-cache'});
    fs.createReadStream(f).pipe(res);
  });
}).listen(8765,'127.0.0.1',()=>console.log('serving '+root+' on 8765'));
