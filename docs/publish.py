import os
import io
import markdown
import datetime

mdpath = os.path.join(os.path.dirname(__file__), '..', 'README.md')
srcpath = os.path.join(os.path.dirname(__file__), 'inde.src.html')
mdf = io.open(mdpath, mode="r", encoding="utf-8")
mdt = mdf.read()
content = markdown.markdown(mdt)

uptime = '2022-02-24 15:57:00'

outt = io.open(srcpath, mode="r", encoding="utf-8").read()
outt = outt.replace('<!-- contant -->', content)
outt = outt.replace('<!-- uptime -->', uptime)


def get_media_html(path, pre=''):
    path = os.path.abspath(path)
    os.path.join(os.path.dirname(__file__), '..', 'README.md')
    eles = []
    for r in sorted(list(os.listdir(path))):
        fpath = os.path.join(path, r)
        rpath = pre + fpath.replace(path, '')
        # fpath = os.path.abspath(fpath)
        if rpath.endswith('jpeg') or rpath.endswith('png') or rpath.endswith('jpg'):
            print(path, fpath, rpath)
            eles.append('<div class="element-item"><img class="image lazyload" data-original="%s"/><span>%s</span></div>' % (rpath, r.split('.')[0].split('-')[-1]))
    return '\n'.join(eles)


xchtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '宣传'), '相关证据/宣传')
outt = outt.replace('<!-- xc -->', xchtml)

sjhtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '实景'), '相关证据/实景')
outt = outt.replace('<!-- sj -->', sjhtml)

outpath = os.path.join(os.path.dirname(__file__), '..', 'index.html')
with io.open(outpath, mode="w", encoding="utf-8") as f:
    f.write(outt)

print(datetime.datetime.now())
