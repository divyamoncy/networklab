#include <semaphore.h>
#include <pthread.h>
#include <stdio.h>
sem_t e,w,m1,m2;
int ecount=0;
int wcount=0;
void *eastfn(void *arg)
{
        int f=(int)arg;
        sem_wait(&m1);
        ecount+=1;
        if(ecount==1)
           sem_wait(&w);
        sem_post(&m1);
        sem_wait(&e);
           printf("Baboon %d crossing eastwards\n",f+1);
        sem_post(&e);
        sem_wait(&m1);
          ecount--;
          if(ecount==0)
               sem_post(&w);
         sem_post(&m1);
}
void *westfn(void *arg)
{
        int f=(int)arg;
        sem_wait(&m2);
        wcount+=1;
        if(wcount==1)
           sem_wait(&e);
        sem_post(&m2);
        sem_wait(&w);
           printf("Baboon %d crossing westwards\n",f+1);
        sem_post(&w);
        sem_wait(&m2);
          wcount--;
          if(wcount==0)
               sem_post(&e);
         sem_post(&m2);
}
int main()
{
        int i;
        pthread_t baboon[10];
        sem_init(&m1,0,1);
        sem_init(&m2,0,1);
        sem_init(&e,0,1);
        sem_init(&w,0,1);
        for(i=0;i<5;i++){
          pthread_create(&baboon[i],NULL,eastfn,(void *)i);
          pthread_create(&baboon[i],NULL,westfn,(void *)(i+5));
        }
         for(i=0;i<5;i++){
          pthread_join(baboon[i],NULL);
          pthread_join(baboon[i],NULL);
        }
        return 0;
}