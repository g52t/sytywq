import os
import io
import markdown
import datetime

mdpath = os.path.join(os.path.dirname(__file__), '..', 'README.md')
srcpath = os.path.join(os.path.dirname(__file__), 'inde.src.html')
mdf = io.open(mdpath, mode="r", encoding="utf-8")
mdt = mdf.read()
content = markdown.markdown(mdt)

outt = io.open(srcpath, mode="r", encoding="utf-8").read()
outt = outt.replace('<!-- contant -->', content)


def get_media_html(path, pre=''):
    path = os.path.abspath(path)
    os.path.join(os.path.dirname(__file__), '..', 'README.md')
    eles = []
    elesp = []
    oths = []
    for r in sorted(list(os.listdir(path))):
        if r[0] == '.':
            continue
        if r.endswith('.md'):
            continue
        fpath = os.path.join(path, r)
        rpath = pre + fpath.replace(path, '')
        # fpath = os.path.abspath(fpath)
        if rpath.endswith('jpeg') or rpath.endswith('png') or rpath.endswith('jpg'):
            # print(path, fpath, rpath)
            eles.append('<div class="element-item image"><img class="lazyload" data-original="%s"/><span>%s</span></div>' % (rpath, r.split('.')[0].split('-')[-1]))
        elif rpath.endswith('mp4'):
            elesp.append('<div class="element-item video"><video src="%s"></video><span>%s<em class="btn-play">播放视频</em></span></div>' % (rpath, r.split('.')[0].split('-')[-1]))
        else:
            oths.append('<a href="%s">《%s》</a>' % (rpath, r.split('-')[-1]))
    return '\n'.join(eles + elesp + oths)


xchtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '宣传'), '相关证据/宣传')
outt = outt.replace('<!-- xc -->', xchtml)

sjhtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '实景'), '相关证据/实景')
outt = outt.replace('<!-- sj -->', sjhtml)

zchtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '法规政策'), '相关证据/法规政策')
outt = outt.replace('<!-- zc -->', zchtml)

dfhtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '答复文件'), '相关证据/答复文件')
outt = outt.replace('<!-- df -->', dfhtml)

wdhtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关文档'), '相关文档')
outt = outt.replace('<!-- wd -->', wdhtml)

uptime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
outt = outt.replace('<!-- uptime -->', uptime)

outpath = os.path.join(os.path.dirname(__file__), '..', 'index.html')
with io.open(outpath, mode="w", encoding="utf-8") as f:
    f.write(outt)

print(uptime)
