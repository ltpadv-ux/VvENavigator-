from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,zipfile
ENGINE_VERSION='3.8.0'
def _sum(p):
 h=sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
def build_release_index(version,vve_name,files,status='GEREED VOOR ALV',history=None):
 items=[]
 for name,path in files.items():
  p=Path(path)
  if p.exists(): items.append({'name':name,'path':str(p),'size':p.stat().st_size,'sha256':_sum(p)})
 return {'release_packaging_version':ENGINE_VERSION,'release_version':version,'vve_name':vve_name,'status':status,'created_at':datetime.now(timezone.utc).isoformat(),'files':items,'file_count':len(items),'history':history or []}
def write_release_package(version,vve_name,files,output_dir='artifacts',status='GEREED VOOR ALV',history=None):
 root=Path(output_dir); root.mkdir(parents=True,exist_ok=True); idx=build_release_index(version,vve_name,files,status,history); base=f'VvE-Navigator-{version}-release'; ip=root/f'{base}.index.json'; sp=root/f'{base}.sha256'; zp=root/f'{base}.zip'; ip.write_text(json.dumps(idx,indent=2,ensure_ascii=False)); sp.write_text('\n'.join(f"{x['sha256']}  {Path(x['path']).name}" for x in idx['files']))
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
  [z.write(x['path'],arcname=Path(x['path']).name) for x in idx['files']]; z.write(ip,arcname=ip.name); z.write(sp,arcname=sp.name)
 return {'status':status,'release_version':version,'index':str(ip),'checksums':str(sp),'distribution_zip':str(zp),'file_count':idx['file_count']}
