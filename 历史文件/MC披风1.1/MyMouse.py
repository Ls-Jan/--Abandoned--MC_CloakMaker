class MyMouse:
    def __init__(self):
        self.FuncRoll=None#�м�����ʱ���õĺ������޲�
        self.FuncDrag=None#�����ק
        self.FuncRelease=None#����ͷ�
        self.FuncClick=None#�������
        self.FuncDoubleClick=None#���˫��
        self.FuncRightClick=None#�Ҽ�����
        self.FuncRightDrag=None#�Ҽ���ק
        self.FuncDoubleRightClick=None#�Ҽ�˫��
        self.OffsetX=0#���Xλ��
        self.OffsetY=0#���Yλ��
        self.RollUp=True#�������Ϲ���
        self.X=0
        self.Y=0
        self.RootX=0
        self.RootY=0
    def __GetOppositeCoord(self,Event):
        return (Event.x_root-self.RootX,Event.y_root-self.RootY)
    def Click(self,Event):
        self.X,self.Y=self.__GetOppositeCoord(Event)
        if(self.FuncClick):
            self.FuncClick()
    def Drag(self,Event):
        oldX,oldY=self.X,self.Y
        self.X,self.Y=self.__GetOppositeCoord(Event)
        self.OffsetX,self.OffsetY=self.X-oldX,self.Y-oldY
        if(self.FuncDrag):
            self.FuncDrag()
    def Release(self,Event):
        self.X,self.Y=self.__GetOppositeCoord(Event)
        if(self.FuncRelease):
            self.FuncRelease()
    def RightClick(self,Event):
        self.X,self.Y=self.__GetOppositeCoord(Event)
        if(self.FuncRightClick):
            self.FuncRightClick()
    def Roll(self,Event):
        if(Event.delta>0):
            self.RollUp=True
        else:
            self.RollUp=False
        if(self.FuncRoll):
            self.FuncRoll()
    def RightDrag(self,Event):
        oldX,oldY=self.X,self.Y
        self.X,self.Y=self.__GetOppositeCoord(Event)
        self.OffsetX,self.OffsetY=self.X-oldX,self.Y-oldY
        if(self.FuncRightDrag):
            self.FuncRightDrag()
    def DoubleClick(self,Event):
        self.X,self.Y=self.__GetOppositeCoord(Event)
        if(self.FuncDoubleClick):
            self.FuncDoubleClick()
    def DoubleRightClick(self,Event):
        self.X,self.Y=self.__GetOppositeCoord(Event)
        if(self.FuncDoubleRightClick):
            self.FuncDoubleRightClick()
