class GuiContext:
    _gui_ref = None

    def __new__(cls):
        pass

    @classmethod
    def set_gui_ref(cls, ref):
        cls._gui_ref = ref

    @classmethod
    def user_feedback(cls, text:str):
        cls._gui_ref(text)



