import os
import io
import markdown
mdpath = os.path.join(os.path.dirname(__file__), '..', 'README.md')
srcpath = os.path.join(os.path.dirname(__file__), 'inde.src.html')
mdf = io.open(mdpath, mode="r", encoding="utf-8")
mdt = mdf.read()
content = markdown.markdown(mdt)

uptime = '2022-02-24 15:57:00'

outt = io.open(srcpath, mode="r", encoding="utf-8").read()
outt = outt.replace('<!-- contant -->', content)
outt = outt.replace('<!-- uptime -->', uptime)

outpath = os.path.join(os.path.dirname(__file__), '..', 'index.html')
with io.open(outpath, mode="w", encoding="utf-8") as f:
	f.write(outt)




