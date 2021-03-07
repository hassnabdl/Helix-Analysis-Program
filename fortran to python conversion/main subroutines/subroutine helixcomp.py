import numpy as np
import math

def helixcomp(nslt,nres,calph0,dir0,perpvec0,start0,en0,cent0,rn0,camod,axfact,calph,dir,perpvec,start,end,cent,anglechange,anglechangeref,axtol,iw0,torsion,rotation,nrep,indexax,incrot,ireorienthx,idebughx,radtodeg, cc2,nreshx,icaahx,ihx,nhxres,maxhx,maxat)
  """
  
  Compute the rotation angle of a helix form the average angle between
  the corresponding perpendiculars to the helix axis from the Calphas

  ***
  Parameters:
  nslt:
  nres:
  calph0:
  dir0:
  perpvec0:
  start0:
  en0: 
  cent0:
  rn0:
  camod:
  axfact:
  calph:
  dir:
  perpvec:
  start:
  end:
  cent:
  anglechange:
  anglechangeref:
  axtol:
  iw0:
  torsion:
  rotation:
  nrep:
  indexax:
  incrot:
  ireorienthx:
  idebughx:
  radtodeg:
  cc2:
  nreshx:
  icaahx:
  ihx:
  nhxres:
  maxhx:
  maxat:

  Returns

  """
  PI = math.pi
  1000  format(' Rotation=',f9.2,' SD=',f7.2,
     -  ' Local tilt=',f9.2,' N/Nr angle:',f8.3,/,
     -  ' X,Y,Z displacements=',3f8.2,' Absolute displacement=',f8.2)
1001  format(' ',a,' helix cent:',3f12.3,/,' Alpha C:',(3f12.3))
      # end    
 
  dimension anglechange(maxhx),anglechangeref(maxhx),indexax(3),
     -  cc2(3,maxat),icaahx(maxhx)
      #real*8 calph0(3,maxhx),dir0(3),start0(3),en0(3),cent0(3),rn0(3),
     -  perpvec0(3,maxhx),camod(3,maxhx),axfact(maxhx),calph(3,maxhx),
     -  dir(3),start(3),# end(3),cent(3),perpvec(3,maxhx)
      parameter (MAXFRAMES=50000,MAXCOPY=600)
      common /analres/ nframe,nframeref,nframetot,maxframe,maxpres,
     -  increment,increment2,res(2,MAXFRAMES,MAXCOPY),
     -  x0(MAXCOPY),y0(MAXCOPY),nxselres,ixselres(MAXCOPY)
      character*2 iatnm2
      common /atnam/ aw(99),nval(99),nvalmax(99),mmofan(99),
     -  mmatno(64),iatnm2(99)
      #real*8 org(3),dev(3),startg(3),# endg(3),circ(3),rn(3),xx(3),yy(3),
     -  startw(3),# endw(3),dirw(3),dirdotdir0,ddot,rms,devs(3),deve(3)
      dimension rot(3,3),corig(3,3),ccurr(3,3),shift(3),angles(3),
     -  anglesn(3)
      character*9 decidebend

  incrhx=(ihx-1)*nhxres
  iverbort=1
  if (nframe  >  10  or  nrep  >  1):
   iverbort=0
  print('HELIXC nframe,nrep,iverbort=',nframe,nrep,iverbort)
  if (nrep  ==  1  and  nframe  ==  1  and  idebughx  >  0):
    print("initial helix cent:",cent0)
    for ir in range(nres):
      for k in range(3):
        print("Alpha C:",calph0[k][ir])
  it=0
  #cc2 will be the possibly translated/overlaid frame
  res =  helixaxis(cc2,nslt,0,calph,dirw,startw,endw,cent,perpvec,camod,anglechangeref,circ,rn,axfact,axtol,rot,rms,helixlen,angles,decidebend,nup,ndown,nrun,nnear,rcirc,turnperres,anglesn,0,incrot,nrep,1,nreshx,icaahx,ihx,nhxres,idebughx,radtodeg,pi,MAXHX)
  start = startw.copy()
  end = endw.copy()
  dir = dirw.copy()
  if (nrep  ==  1  and  idebughx  >  0):
    print("current helix cent:",cent)
    for ir in range(res):
      for k in range(3):
        print("Alpha C",calph[k][ir])
  #Shift the helix so that the start is at the origin
  for ir in range(nres):
    calph[0][ir] = calph[0][ir] - start
  end = end - start  
  for k in range(3):
    shift[k]=start[k]
    start = 0
    startg = start.copy()
    endg = end.copy()
  if (nrep  ==  1) :
    dirdotdir0 = np.dot(dir,dir0)
    try :
      rotation = dacoscheck(dirdotdir0)
    except:
      print("Error in dacoscheck rotation =",dirdotdir0)
    res[0][nframe][incrhx+5] = math.cos(rotation)
    res[1][nframe,incrhx+5]=sin(rotation)
    dev = cent - cent0
    res[0][nframe][incrhx+8] = math.sqrt(np.dot(dev,dev))
    res[1][nframe][incrhx+8]=dev[indexax[0]]
    res[0][nframe][incrhx+9]=dev[indexax[1]]
    res[1][nframe][incrhx+9]=dev[indexax[2]]
    devs = startw - start0
    res[0][nframe][incrhx+10]=devs[indexax[1]]
    res[1][nframe][incrhx+10]=devs[indexax[2]]
    deve = endw - en0
    res[0][nframe][incrhx+11]=deve[indexax[1]]
    res[1][nframe][incrhx+11]=deve[indexax[2]]
    if (idebughx  >  0  and  dirdotdir0  >  0.001):
      print("current helix cent",cent)
      for ir in range(nres):
        for k in range(3):
          print("Alpha C:",calph[k][ir])
    if (ireorienthx  ==  1):
    #For better result, rotate dir onto dir0. The rotation axis is the
    #normal to the dir0-dir plane         
    org = np.cross(dir0,dir)
    for k in range(3):
      corig[k][0]=0.0
      ccurr[k][0]=0.0
      corig[k][1]=dir0[k]
      ccurr[k][1]=dir[k]
      corig[k][2]=org[k]
      ccurr[k][2]=org[k]
    rot = ormat(ccurr,corig,3,iverbort)
    for ir in range(nres):
      calph[0][ir] = dsmatvec(rot,calph(1,ir))
    dir = dir0.copy()
    if (idebughx  >  0):
      print("current reoriented helix cent:",cent)
    for ir in range(nres):
      for k in range(3):
        print("Alpha C:",calph[k][ir])
    for ir in range(0, nres):
      perpvec[0][ir], org = calcperp(start, dir, calph[0][ir], it)
    nflip=0
    rotav=0
    rotav2=0
    changemin=100.0
    changemax=0.0
    nflipprev=nflip
    print("NRES-",nres)
    for ir in range(nres):
      angchange = angcomp(perpvec0[0][ir],dir0,perpvec[0][ir])
      print("ir={} dang = {} ".format(ir,angchange))
      for k in range(3):
        print("dir0 = {} perpvec = {} perpvec0 = {}".format(dir0[k],perpvec[k][ir],perpvec0[k][ir]))
      rotav+=angchange
      rotav2+=angchange**2
      if (angchange < changemin):
        changemin = angchange
      if (angchange > changemax):
        changemax = angchange
      angchange[ir] = angchange  

    torsion=rotav/nres
    sd=math.sqrt(abs(rotav2/nres-torsion**2))



cd77        write (77,6533) nframe,torsion*180.0/pi,changemin*180.0/pi,
cd77     -    changemax*180.0/pi,(anglechange(ir)*180.0/pi,ir=1,nres)
cd776533    format(' Nframe=',i6,' avg,min,max=',3f10.3,/,(10f8.2))
        if (changemax-changemin  >  pi/2.0) :
c         Likely to have some sign flips
          for ir in range(0, nres):
            for k in range(0, 3):
              xx(k)=-perpvec(k,ir)
            
            call angcomp(perpvec0(1,ir),dir0,xx,angchange)
            if (abs(angchange-torsion)  < 
     -        abs(anglechange(ir)-torsion)) :
              call trnsfrd(perpvec(1,ir),xx,3)
              nflip=nflip+1
            ## end if
          
          if (nflip  <=  nres  and  nflip  >  nflipprev) go to 100
        ## end if
        if (nflip  >  0) :
c         Recalculate TPR
          call calcturnperres(turnperres,nres,incrot,perpvec,dir,
     -      anglechangeref,1,pi,MAXHX)
          res(1,nframe,incrhx+6)=cos(turnperres)
          res(2,nframe,incrhx+6)=sin(turnperres)
        ## end if
        res(1,nframe,incrhx+4)=cos(torsion)
        res(2,nframe,incrhx+4)=sin(torsion)
        call dcross(dir0,rn0,xx)
        call dcross(rn0,xx,yy)
        for k in range(0, 3):
          rot(1,k)=yy(k)
          rot(2,k)=xx(k)
          rot(3,k)=rn0(k)
        
c       Keep the normal from oscillating 180 degrees
        if (ddot(rn,rn0)  <  0.0) call dvmul(rn,-1.00,rn)
        call dsmatvec(rot,rn,xx)
        res(1,nframe,incrhx+12)=xx(1)
        res(2,nframe,incrhx+12)=xx(2)
        call printhelix(iw0,startw,# endw,cent,rms,helixlen,dirw,angles,
     -    decideb# end,nup,ndown,nrun,nnear,rcirc,turnperres,anglesn,ihx,
     -    radtodeg)
        rn_rn0=radtodeg*dacoscheck(ddot(rn,rn0),ccc,1,6,'HELIXNORMALS')
        write (iw0,1000) radtodeg*torsion,radtodeg*sd,radtodeg*rotation,
     -    rn_rn0,dev,math.sqrt(ddot(dev,dev))
      ## end if
      if (nrep  <  0) return
      return
1000  format(' Rotation=',f9.2,' SD=',f7.2,
     -  ' Local tilt=',f9.2,' N/Nr angle:',f8.3,/,
     -  ' X,Y,Z displacements=',3f8.2,' Absolute displacement=',f8.2)
1001  format(' ',a,' helix cent:',3f12.3,/,' Alpha C:',(3f12.3))
      # end    
 

      
