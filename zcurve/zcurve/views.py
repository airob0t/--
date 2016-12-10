from django.shortcuts import render
from django.http import HttpResponse
from uuid import uuid1
from models import result
from gen.settings import RESULT_IN, RESULT_OUT, BASE_DIR
from django.http import StreamingHttpResponse
import subprocess
import os


# Create your views here.

def index(request):
    return render(request, 'index.html')


def upload(request):
    extin = '.in'
    extout = '.out'
    exepath = 'util'
    exepath = os.path.join(BASE_DIR, exepath)
    exename = 'zcurve3.0.exe'
    fname = str(uuid1())
    inpath = os.path.join(RESULT_IN, fname + extin)
    outpath = os.path.join(RESULT_OUT, fname + extout)
    sequence = request.POST.get('sequence', '')
    infile = request.FILES.get('file', '')

    if sequence == '' and infile == '':
        return HttpResponse('Please input the data!')
    elif sequence != '' and infile != '':
        return HttpResponse('Please do not input and upload sequence at the same time!')
    else:
        if sequence != '':
            f = open(inpath, 'w')
            f.write(sequence)
            f.close()
        else:
            f = open(inpath, 'wb')
            for chunk in infile.chunks():
                f.write(chunk)
            f.close()
        mtag = request.POST.get('format', '')
        predict = request.POST.get('predict','')
        genes = request.POST.get('genes', '')
        protein = request.POST.get('protein', '')
        essential = request.POST.get('essential', '')
        essential = ''
        if mtag != 'LST':
            if predict != '':
                subprocess.call([os.path.join(exepath, exename), inpath, outpath, '-m'], cwd=exepath)
            if genes != '':
                subprocess.call([os.path.join(exepath, exename), inpath, outpath + '.fnn', '-m', '-n'], cwd=exepath)
            if protein != '':
                subprocess.call([os.path.join(exepath, exename), inpath, outpath + '.faa', '-m', '-p'], cwd=exepath)
        else:
            if predict != '':
                subprocess.call([os.path.join(exepath, exename), inpath, outpath], cwd=exepath)
            if genes != '':
                subprocess.call([os.path.join(exepath, exename), inpath, outpath + '.fnn', '-n'], cwd=exepath)
            if protein != '':
                subprocess.call([os.path.join(exepath, exename), inpath, outpath + '.faa', '-p'], cwd=exepath)

        # if essential != '':    #take a long time
        #    subprocess.Popen([os.path.join(exepath, exename), inpath, outpath+'.ess', '-e'], cwd=exepath)
        # subprocess.call([os.path.join(exepath, exename), inpath, outpath,mtag,genes,protein,essential], cwd=exepath)

        html = '''
        <html>
<head></head>
<body>

<table width="750" align="center">
<tbody>
<tr><td bgcolor="#A0B8C8"><font color="white"><b> &nbsp; &nbsp; Gene Prediction Results </b></font></td></tr>
<tr><td><p align="center"><a href="/">Click here to submit another sequences.</a></p>
<table border="1" align="center">
<tbody><tr><th> output </th><th> link </th></tr>

<tr><td> Coordinates of predicted genes </td><td> <a href="/result/?uid={0}"><b> gms.out </b></a> </td></tr>
<tr><td> Gene sequences </td><td> <a href="/result/?uid={0}&ext=fnn"><b> gms.out.fnn </b></a> </td></tr>
<tr><td> Protein sequence </td><td> <a href="/result/?uid={0}&ext=faa"><b> gms.out.faa </b></a> </td></tr>
<tr><td>Essential Genes</td><td><a href="/result/?uid={0}&ext=ess"><b> gms.out.ess </b></a> </td></tr>

<tr></tr>
</tbody>
</table>
</td></tr>
</tbody>
</table>

</body>
</html>
        '''.format(fname)

        return HttpResponse(html)


def result(request):
    uid = request.GET.get('uid','')
    ext = request.GET.get('ext','')
    fname = uid+'.out'
    if ext != '':
        fname = fname+'.'+ext
    fname = fname.replace('/','').replace('\\','')
    outpath = os.path.join(RESULT_OUT,fname)
    if not os.path.exists(outpath):
        return HttpResponse('Not exist this file.')

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(outpath))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fname)
    return response

def example(request):
    return render(request,'data.html')