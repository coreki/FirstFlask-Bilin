

def select(user):
    print user
    pwd = user+'123'

    def go(show):
        show(pwd)

    return go

@select('core')
def showpwd(pwd):
    print 'pwd is %s' % pwd