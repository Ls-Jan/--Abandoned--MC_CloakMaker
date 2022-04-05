from math import cos,sin,tan
import numpy as np
import cv2

class Block:#����
    SurfaceToPoints={'Front':(0,1,2,3),'Back':(4,5,6,7),'Left':(7,6,1,0),'Right':(3,2,5,4),'Up':(7,0,3,4),'Down':(1,6,5,2)}#����Ӧ��ϵ(���Ǵ�˳���
    SurfacePoints={'Front':0x0F,'Back':0xF0,'Left':0xC3,'Right':0x3C,'Up':0x99,'Down':0x66}#����,�����ж��ĸ������ǵĵ������������ǲ�����ʾ�ġ���λ�ж�(���죬��ˬ
    def __init__(self,points,cvImgs):
    #pointsΪ�б��Ƿ���İ˸�����(��ԪԪ��)���ֱ���ǰ����ĸ�����ͺ�����ĸ����㣬˳��Ϊ�����Ͻǿ�ʼ����ʱ��
    #points:[����(ǰ),����(ǰ),����(ǰ),����(ǰ),����(��),����(��),����(��),����(��)]
    #cvImgs:Ϊ�б��Ƿ���������棬��þʹ�С����㣬Ҫ��Ȼ���÷��鲻�պϻ��߷���ĳ���������ͼƬ��ʽΪcv2��ȡ��ͼƬ
    #cvImgs:[ǰ,��,��,��,��,��]�����ĳ���治��Ҫͼ��ֱ��None
        self.points=[]
        for P in points:
            self.points.append(list(P)+[1])#������4ά����
        self.points=np.matrix(self.points)#�����ɾ��󣬷�������
        self.imgs={}
        for key in ['Front','Back','Left','Right','Up','Down']:
            self.imgs[key]=cvImgs[len(self.imgs)]
    def GetMatrix(Camera,ViewSize):#�������λ�÷��ر任����
        sinA=sin(Camera.a)
        sinB=sin(Camera.b)
        cosA=cos(Camera.a)
        cosB=cos(Camera.b)
        r=Camera.r

        Matrix=np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[r*cosA*cosB,r*sinA*cosB,r*sinB,1]])#ͶӰ�����ƶ���ԭ��
        Matrix=Matrix*np.matrix([[cosA,-sinA,0,0],[sinA,cosA,0,0],[0,0,1,0],[0,0,0,1]])#��zת��-a�Ƕ�
        Matrix=Matrix*np.matrix([[sinB,0,cosB,0],[0,1,0,0],[-cosB,0,sinB,0],[0,0,0,1]])#��yת��pi/2-b�Ƕ�
        Matrix=Matrix*np.matrix([[0,-1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])#��zת��-pi/2�Ƕ�
        
        d_CameraToView=20#��ͷ���۲�����롣�۲�����ǰ�����ľ���̶�Ϊ0.8*d�������Ϊɶ���Ӳ������á�
        Matrix=Matrix*np.matrix([[(10/9)/ViewSize[0],0,0,0],[0,(10/9)/ViewSize[1],0,0],[0,0,(5/9)/d_CameraToView,0],[0,0,0,1]])#�����任��ɹ淶��͸��ͶӰ
        Matrix=Matrix*np.matrix([[1,0,0,0],[0,1,0,0],[0,0,2.5,1],[0,0,-1.5,0]])#�任�ɹ淶��ƽ��ͶӰ
        return Matrix
    def GetImg(self,Camera,VSize):#ת��ͼƬ����ȡӳ��仯���ͼƬ����ʽ��Ϊcv2(��ʽ�Լ�ת���Ϳɴ�canvas����ʾ
        VSizeHalf=(int(VSize[0]/2),int(VSize[1]/2))
        TM=Block.GetMatrix(Camera,VSize)*100*Camera.r#ת������(˳���������Ŵ�һ��

        Points=[]#ȡ��ת����ĵ�
        for P in self.points*TM:
            Points.append((VSizeHalf[0]+P[(0,0)],VSizeHalf[1]+P[(0,1)],P[(0,2)]))#ȡ��P������
        nullP=[0]#�����ǵĵ�(��Ȼ��һ�������п����ж�����������б�
        for pst in range(8):
            dist=Points[pst][2]-Points[nullP[0]][2]
            if dist==0:
                nullP.append(pst)
            elif dist<0:
                nullP=[pst]
        if(nullP.count(0)==2):#�����䷭���¹ʡ�
            nullP.remove(0)
        nullP.append(0)
        for pst in nullP[:-1]:#Ҳ�ǽ���ת��Ϊλ�ķ�ʽ��һ�������ɡ��������졢��ˬ
            nullP[-1]+=(1<<pst)
        nullP=nullP[-1]
        
        targetImg=np.zeros((VSize[0],VSize[1],3),np.uint8)
        for key in self.imgs:#�����ʾͼƬ
            if(Block.SurfacePoints[key]&nullP):#��������˾�˵��������ж�������Ч�ģ�������治��Ҫ��ʾ
                continue
            if(type(self.imgs[key]) is not np.ndarray):#����ǿյ��Ǿ���������
                continue
            args=self.imgs[key].shape#ͼƬ�ĳ���
            before=np.float32([[args[1],0],[args[1],args[0]],[0,args[0]]])#ȡ3����͹���
            after=[]
            for i in Block.SurfaceToPoints[key][:3]:
                after.append([Points[i][0],Points[i][1]])
            after=np.float32(after)
            targetImg=cv2.add(targetImg,cv2.warpAffine(self.imgs[key],cv2.getAffineTransform(before,after),tuple(VSize)))#����任������������뵽targetImg��
        return targetImg
    def LoadImg(self,surfaceName,cvImg):
        if(type(self.imgs.get(surfaceName)) !=type(None)):
            self.imgs[surfaceName]=cvImg

