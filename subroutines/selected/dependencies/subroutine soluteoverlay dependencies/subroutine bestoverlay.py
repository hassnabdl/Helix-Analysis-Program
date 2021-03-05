      def bestoverlay(nat,index1,index2,c1,c2,atw,atwsuminp,
     -  cc1,cc2,atw1,rot,com1,com2,LEVTEST,TOLERANCE,iout,maxat)
      dimension index1(maxat),index2(maxat),c1(3,maxat),c2(3,maxat),
     -  atw(maxat),cc2(3,maxat),cc1(3,maxat),atw1(maxat),
     -  rot(3,3),com1(3),com2(3)
c     For the atoms in c1(index1(i)), c2(index2(i)) get the best fit
c     using the algorithm of Kabasch, Acta Cryst, A32, p922 (1976).
c     c1 is assumed to be the reference structure.
c     cc1,cc2 are used for temporary storage
      dimension ijk(3,2)
      #real*8 atwsuminp,atwsum,sm,r(3,3),dcom1(3),dcom2(3),
     -  rr(3,3),diag(3),offdiag(3),a(3,3),b(3,3),rmu(3)
      data iz /0/,inz /0/,atwsum /0.0/
c     print *,'BESTOVERLAY LEVTEST,maxat,nat=',LEVTEST,maxat,nat
      ijk(1,1)=2
      ijk(1,2)=3
      ijk(2,1)=1
      ijk(2,2)=3
      ijk(3,1)=1
      ijk(3,2)=2
      devmax=0.0
      if (nat  ==  1) return
c     Move both sets into COM frame
      for k in range(0, 3):
        dcom1(k)=0.0
        dcom2(k)=0.0
      
      for i in range(0, nat):
        atw1(i)=atw(index1(i))
        for k in range(0, 3):
          cc1(k,i)=c1(k,index1(i))
          cc2(k,i)=c2(k,index2(i))
          dcom1(k)=dcom1(k)+atw1(i)*cc1(k,i)
          dcom2(k)=dcom2(k)+atw(index2(i))*cc2(k,i)
        
      
c     write (77,7831) 'INDEX1',(index1(i),i=1,nat)
c     write (77,7831) 'INDEX2',(index2(i),i=1,nat)
c7831 format(1x,a,':',/,(20i5))
c     write (77,7832) 'CC1',(i,(cc1(k,i),k=1,3),i=1,nat)
c     write (77,7832) 'CC2',(i,(cc2(k,i),k=1,3),i=1,nat)
c7832 format(1x,a,':',/,(i5,3f10.5))
      if (atwsuminp  ==  0.0) :
        atwsum=0.0
        for i in range(0, nat):
          atwsum=atwsum+atw1(i)
        
      else:
        atwsum=atwsuminp
      ## end if
      for k in range(0, 3):
        com1(k)=dcom1(k)/atwsum
        com2(k)=dcom2(k)/atwsum
      
      if (LEVTEST  >  0) write (LEVTEST,1001) atwsum,com1,com2
      for i in range(0, nat):
        for k in range(0, 3):
          cc1(k,i)=cc1(k,i)-com1(k)
          cc2(k,i)=cc2(k,i)-com2(k)
        
      
c     Calculate coordinate sums - Numerical recipes starts arrays from 1##
      for k in range(0, 3):
        for l in range(0, 3):
          r(k,l)=0.0
          for i in range(0, nat):
            r(k,l)=r(k,l)+atw1(i)*cc1(k,i)*cc2(l,i)
          
          r(k,l)=r(k,l)/atwsum
        
      
      for k in range(0, 3):
        for l in range(0, 3):
          sm=0.0
          for m in range(0, 3):
            sm=sm+r(m,k)*r(m,l)
          
          rr(k,l)=sm
        
      
      if (LEVTEST  >  0) :
        write (LEVTEST,1000) "r",r
        write (LEVTEST,1000) "rr",rr
      ## end if
c     Find the eigenvectors a and eigenvalues mu of rr
      call dtred2(rr,3,3,diag,offdiag)
      call dtqli(diag,offdiag,3,3,rr,ierr)
      if (ierr  >  0) :
        write (6,1004)
        if (iout  >  0) write (iout,1004)
        return
      ## end if
1004  format(' Calculation aborted due to diagonalization failure')
      for k in range(0, 3):
        for l in range(0, 3):
          a(k,l)=rr(l,k)
        
      
c     The rows of the matrix a are the eigenvectors
c     Calculate rotation matrix (U in Kabasch's notation)
      nz=0
      for k in range(0, 3):
        if (abs(diag(k))  >  TOLERANCE) :
          rmu(k)=math.sqrt(abs(diag(k)))
        else:
          rmu(k)=0.0
          nz=nz+1
        ## end if
      
      if (LEVTEST  >  0) write (LEVTEST,*) "mu=",rmu
      for k in range(0, 3):
        if (rmu(k)  <  TOLERANCE) :
          iz=k
        else:
          for l in range(0, 3):
            sm=0.0
            for m in range(0, 3):
              sm=sm+r(l,m)*a(k,m)
            
            b(k,l)=sm/rmu(k)
          
          inz=k
        ## end if
      
      if (LEVTEST  >  0) write (LEVTEST,*) "nz=",nz
      if (nz  ==  1) :
c       Planar molecule: a(iz)=a(inz)xa(jnz), same for b
         a(iz,1)=a(ijk(iz,1),2)*a(ijk(iz,2),3)-
     -     a(ijk(iz,1),3)*a(ijk(iz,2),2)
         a(iz,2)=a(ijk(iz,1),3)*a(ijk(iz,2),1)-
     -     a(ijk(iz,1),1)*a(ijk(iz,2),3)
         a(iz,3)=a(ijk(iz,1),1)*a(ijk(iz,2),2)-
     -     a(ijk(iz,1),2)*a(ijk(iz,2),1)
         b(iz,1)=b(ijk(iz,1),2)*b(ijk(iz,2),3)-
     -     b(ijk(iz,1),3)*b(ijk(iz,2),2)
         b(iz,2)=b(ijk(iz,1),3)*b(ijk(iz,2),1)-
     -     b(ijk(iz,1),1)*b(ijk(iz,2),3)
         b(iz,3)=b(ijk(iz,1),1)*b(ijk(iz,2),2)-
     -     b(ijk(iz,1),2)*b(ijk(iz,2),1)
      elif (nz  ==  2) :
c       Linear molecules
c       First set the iz-th components to nonparalel to the inz-th
        for k in range(0, 3):
          a(iz,k)=0.0
          b(iz,k)=0.0
        
        if (abs(a(inz,1))  <  TOLERANCE) :
          a(iz,1)=rmu(inz)
        elif (abs(a(inz,2))  >=  TOLERANCE) :
          a(iz,1)= -a(inz,1)
        else:
          a(iz,2)=rmu(inz)
        ## end if
        if (abs(b(inz,1))  <  TOLERANCE) :
          b(iz,1)=rmu(inz)
        elif (abs(b(inz,2))  >=  TOLERANCE) :
          b(iz,1)= -b(inz,1)
        else:
          b(iz,2)=rmu(inz)
        ## end if
        if (iz  ==  ijk(inz,1)) :
          jz=ijk(inz,2)
        else:
          jz=ijk(inz,1)
        ## end if
c       a(jz)=a(inz)xa(iz)
        a(jz,1)=a(ijk(jz,1),2)*a(ijk(jz,2),3)-
     -    a(ijk(jz,1),3)*a(ijk(jz,2),2)
        a(jz,2)=a(ijk(jz,1),3)*a(ijk(jz,2),1)-
     -    a(ijk(jz,1),1)*a(ijk(jz,2),3)
        a(jz,3)=a(ijk(jz,1),1)*a(ijk(jz,2),2)-
     -    a(ijk(jz,1),2)*a(ijk(jz,2),1)
        b(jz,1)=b(ijk(jz,1),2)*b(ijk(jz,2),3)-
     -    b(ijk(jz,1),3)*b(ijk(jz,2),2)
        b(jz,2)=b(ijk(jz,1),3)*b(ijk(jz,2),1)-
     -    b(ijk(jz,1),1)*b(ijk(jz,2),3)
        b(jz,3)=b(ijk(jz,1),1)*b(ijk(jz,2),2)-
     -    b(ijk(jz,1),2)*b(ijk(jz,2),1)
c       a(iz)=a(inz)xa(jz)
        a(iz,1)=a(ijk(iz,1),2)*a(ijk(iz,2),3)-
     -    a(ijk(iz,1),3)*a(ijk(iz,2),2)
        a(iz,2)=a(ijk(iz,1),3)*a(ijk(iz,2),1)-
     -    a(ijk(iz,1),1)*a(ijk(iz,2),3)
        a(iz,3)=a(ijk(iz,1),1)*a(ijk(iz,2),2)-
     -    a(ijk(iz,1),2)*a(ijk(iz,2),1)
        b(iz,1)=b(ijk(iz,1),2)*b(ijk(iz,2),3)-
     -    b(ijk(iz,1),3)*b(ijk(iz,2),2)
        b(iz,2)=b(ijk(iz,1),3)*b(ijk(iz,2),1)-
     -    b(ijk(iz,1),1)*b(ijk(iz,2),3)
        b(iz,3)=b(ijk(iz,1),1)*b(ijk(iz,2),2)-
     -    b(ijk(iz,1),2)*b(ijk(iz,2),1)
      ## end if
      if (LEVTEST  >  0) :
        write (LEVTEST,*) "diag: ",diag
        write (LEVTEST,*) "mu: ",rmu
      ## end if
      if (LEVTEST  >  0) :
        write (LEVTEST,1000) "a",a
        write (LEVTEST,1000) "b",b
      ## end if
      for k in range(0, 3):
        for l in range(0, 3):
          sm=0.0
          for m in range(0, 3):
            sm=sm+b(m,k)*a(m,l)
          
          rot(k,l)=sm
        
      
      if (LEVTEST  >  0) write (LEVTEST,1000) "rot",rot
      call check_rotmat(rot,'KABSCH',6,ifail,LEVTEST)
      if (ifail  >  0) write (6,1002) diag,rmu
      return
1000  format(' BESTOV ',a,/,(3f16.7))
1001  format(' BESTOV atwsum=',e15.7,' com1=',3f12.7,' com2=',3f12.7)
1002  format(' BESTOV diag=',3e15.7,' mu=',3e15.7)
      # end
