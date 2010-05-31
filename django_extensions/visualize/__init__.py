import pygraphviz


def output(file, dotdata, **kwargs):
    vizdata = ' '.join(dotdata.split("\n")).strip().encode('utf-8')
    version = pygraphviz.__version__.rstrip("-svn")
    try:
        if [int(v) for v in version.split('.')]<(0,36):
            # HACK around old/broken AGraph before version 0.36 (ubuntu ships with this old version)
            import tempfile
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write(vizdata)
            tmpfile.seek(0)
            vizdata = tmpfile.name
    except ValueError:
        pass

    graph = pygraphviz.AGraph(vizdata)
    graph.layout(prog=kwargs['layout'])
    graph.draw(file, format=kwargs.get('format'))
