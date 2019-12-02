
from rp import *
import math
from vispy import app,gloo

class Canvas(app.Canvas):

    def __init__(self,*args,**kwargs):
        app.Canvas.__init__(self,*args,**kwargs)
        self._timer=app.Timer('auto',connect=self.on_timer,start=True)
        self.tick=0
    def on_draw(self,event):
        gloo.clear(color=True)
    def on_timer(self,event):
        global greg
        self.tick+=1 / 60.0
        c=abs(math.sin(self.tick))
        gloo.set_clear_color((c,c,greg,1))
        self.update()
greg=.4
if __name__ == '__main__':
    canvas=Canvas(keys='interactive',always_on_top=True)
    canvas.show()

def vispar():
    def _exeval(f,*x,**y):
        nonlocal _error
        assert _done == _todo == []
        # _todo.insert(0,fog(print,'Hello wurlzy'))
        _todo.insert(0,fog(f,*x,**y))
        while not _done and not _error:
            pass
        assert _todo == []
        if _error:
            assert not _done
            temp=_error
            _error=None
            raise temp
        out=_done.pop()
        assert not _done
        return out
    def _exec(*x,**y):
        return _exeval(exec,*x,**y)
    def _eval(*x,**y):
        return _exeval(eval,*x,**y)

    _error=None
    _todo=[]
    _done=[]  # Results of _todo

    import rp.r_iterm_comm as ric
    _level=ric.pseudo_terminal_level
    run_as_new_thread(pseudo_terminal,globals(),exec=_exec,eval=_eval)
    while ric.pseudo_terminal_level==_level:
        pass
    while 1:
        if ric.pseudo_terminal_level==_level:
            break
        try:
            from vispy import app
            app.process_events()
        except:
            print("harry potwar strikes again! keep chuggin...")
            pass
        if _todo:
            try:
                _done.append(_todo.pop()())
            except BaseException as e:
                _error=e
        assert not _todo
    print('...aaaannndddd were DONE chuggin.')
    app.quit()  # NOT nessecary but PERHAPS its nicer than having a crashy window...make this optional though!!!

vispar()
