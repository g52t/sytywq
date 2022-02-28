import os
import io
import re
import markdown
import datetime


def get_img_with_width(img, width=0, height=0, mode='limit'):
    from PIL import Image
    (bw, bh) = img.size
    if mode == 'fit' and width and height and bw and bh:
        # 等比例缩放
        ss = float(bw) / bh
        ds = float(width) / height
        if ss > ds:
            # 太宽
            nw = int(bh * ds)
            ow = (bw - nw) / 2
            img = img.crop((ow, 0, bw - ow, bh), )
            bw = nw
        elif ds > ss:
            # 太高
            nh = int(bw / ds)
            oh = (bh - nh) / 2
            img = img.crop((0, oh, bw, bh - oh), )
            bh = nh
    if mode == 'limit':
        # 现在最大
        ss = float(bw) / bh
        ds = float(width) / height
        if ss > ds:
            # 太宽
            bw = width
            bh = int(bw / ss) or 1
            img = img.resize((bw, bh), Image.ANTIALIAS)
        elif ds > ss:
            # 太高
            bh = height
            bw = int(bh * ss) or 1
            img = img.resize((bw, bh), Image.ANTIALIAS)
    elif width and bw != width:
        if not height:
            height = int(float(bh) * float(width) / float(bw))
        img = img.resize((width, height), Image.ANTIALIAS)
    return img


def get_file_md5(path):
    import hashlib
    with open(path, 'rb') as fp:
        data = fp.read()
    return hashlib.md5(data).hexdigest()


def get_img_thumb(path, thumbpath, width=300):
    from PIL import Image
    tn = get_file_md5(path) + '-p.jpeg'
    tp = os.path.join(thumbpath, tn)
    if not os.path.exists(tp):
        img = Image.open(path)
        nimg = get_img_with_width(img, width=width, height=width)
        if nimg.mode != 'RGB':
            nimg = nimg.convert('RGB')
        nimg.save(tp)
    return tn


def get_voide_thumb(path, thumbpath, width=300):
    with open(path, 'rb') as fp:
        data = fp.read()
    tn = get_file_md5(path) + '-v.jpeg'
    tp = os.path.join(thumbpath, tn)
    if not os.path.exists(tp):
        from PIL import Image
        tmpp = '/tmp/' + tn
        cmd = 'ffmpeg -i %s -vframes 1 -y %s' % (
            os.path.abspath(path),
            tmpp
        )
        print(cmd)
        r = os.system(cmd)
        print(r)
        # rt = os.popen(cmd).readlines()
        img = Image.open(tmpp)
        nimg = get_img_with_width(img, width=width, height=width)
        if nimg.mode != 'RGB':
            nimg = nimg.convert('RGB')
        nimg.save(tp)
    return tn


# from PIL import Image
#
# img = Image.open('/Users/robin/DO/GitHub/sytywq/相关证据/实景/实景-道路3.jpeg')
# nimg = get_img_with_width(img, width=300, height=300)
# img.show()
# nimg.show()
# exit()

mdpath = os.path.join(os.path.dirname(__file__), '..', 'README.md')
srcpath = os.path.join(os.path.dirname(__file__), 'inde.src.html')
mdf = io.open(mdpath, mode="r", encoding="utf-8")
mdt = mdf.read()
content = markdown.markdown(mdt)

outt = io.open(srcpath, mode="r", encoding="utf-8").read()
outt = outt.replace('<!-- contant -->', content)

thumbpath = os.path.join(os.path.dirname(__file__), 'thumb')


def get_media_html(path, pre='', orderby=''):
    path = os.path.abspath(path)
    os.path.join(os.path.dirname(__file__), '..', 'README.md')
    eles = []
    elesp = []
    oths = []
    files = sorted(list(os.listdir(path)))
    if orderby == 'time':
        files = sorted(files, key=lambda r: os.path.getmtime(os.path.join(path, r)))
    if orderby == '-time':
        files = sorted(files, key=lambda r: os.path.getmtime(os.path.join(path, r)), reverse=True)
    all = []
    for r in files:
        if r[0] == '.':
            continue
        if r.endswith('.md'):
            continue
        if '-raw' in r:
            continue
        fpath = os.path.join(path, r)
        rpath = pre + fpath.replace(path, '')
        # fpath = os.path.abspath(fpath)
        if rpath.endswith('jpeg') or rpath.endswith('png') or rpath.endswith('jpg'):
            # print(path, fpath, rpath)
            thumb = 'docs/thumb/' + get_img_thumb(fpath, thumbpath)
            ele = '<div class="element-item image"><img class="lazyload" v-src="%s" data-original="%s"/><span>%s</span></div>' % (rpath, thumb, r.split('.')[0].split('-')[-1])
            eles.append(ele)
            all.append(ele)
        elif rpath.endswith('mp4'):
            thumb = 'docs/thumb/' + get_voide_thumb(fpath, thumbpath)
            ele = '<div class="element-item video"><video src="%s" poster="%s"></video><span>%s<em class="btn-play">播放视频</em></span></div>' % (rpath, thumb, r.split('.')[0].split('-')[-1])
            elesp.append(ele)
            all.append(ele)
        else:
            ele = '<div class="element-item file"><a href="%s">《%s》</a></div>' % (rpath, r.split('-')[-1])
            oths.append(ele)
            all.append(ele)
    return '\n'.join(all if orderby else (eles + elesp + oths))


xchtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '宣传'), '相关证据/宣传')
outt = outt.replace('<!-- xc -->', xchtml)

sjhtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '实景'), '相关证据/实景')
outt = outt.replace('<!-- sj -->', sjhtml)

zchtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '法规政策'), '相关证据/法规政策', orderby='time')
outt = outt.replace('<!-- zc -->', zchtml)

dfhtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '答复文件'), '相关证据/答复文件', orderby='time')
outt = outt.replace('<!-- df -->', dfhtml)

wdhtml = get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关文档'), '相关文档', orderby='time')
outt = outt.replace('<!-- wd -->', wdhtml)

outt = outt.replace('<!-- xx -->', get_media_html(os.path.join(os.path.dirname(__file__), '..', '相关证据', '进度', '学校'), '相关证据/进度/学校', orderby='time'))

outt = outt.replace('<code>', '<pre class="code">').replace('</code>', '</pre>')

uptime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
outt = outt.replace('<!-- uptime -->', uptime)

for t in re.findall('<img alt="[^"]+" src="[^"]+"[^>]*>', outt):
    rs = re.findall('<img alt="([^"]+)" src="([^"]+)"', t)
    if rs:
        rs = rs[0]
        alt = rs[0]
        img = rs[1]
        fpath = os.path.join(os.path.abspath(os.path.dirname(mdpath)), *img.split('/'))
        thumb = 'docs/thumb/' + get_img_thumb(fpath, thumbpath)
        imgh = '<div class="element-item image"><img class="lazyload" v-src="%s" data-original="%s"/><span>%s</span></div>' % (img, thumb, alt)
        outt = outt.replace(t, imgh)

outpath = os.path.join(os.path.dirname(__file__), '..', 'index.html')
with io.open(outpath, mode="w", encoding="utf-8") as f:
    f.write(outt)

print(uptime)
