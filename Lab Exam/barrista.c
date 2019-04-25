#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdlib.h>

int custcount=0,seqcount=0,eventcount=0;
sem_t m1,m2,cust;
/*  custcount - to keep customer count
    seqcount - to keep sequencer value
    eventcount - to keep event counter value
    m1 - to protect custcount
    m2 - to protect eventcount
    cust - to show there is a customer */


void *customer(void *args)
{
    int f=(int)(args);
    int ticketno;
    sem_wait(&m1);//waiting for semaphore to update custcount
    custcount++;
    if(custcount==1)
       sem_post(&cust);
    ticketno=++seqcount; //giving ticketcount
    printf("Customer with ticketno %d placed order\n",ticketno);
    sem_post(&m1); // releasing m1
    while(eventcount!=ticketno); // waiting till his event number is called out
    sem_wait(&m1); // waiting for m1
    custcount--; // decrementing customer count
    printf("Customer with ticketno %d leaves\n",ticketno);
    sem_post(&cust); // releasing customer
    sem_post(&m1); // releasing m1
    count++;
}
void *barrista(void *args)
{
    while(1)
    {
       sem_wait(&cust); //waiting for customer
       sem_wait(&m2); // waiting for m2
       eventcount++; //updating event count
       if(eventcount>seqcount) // exit condition
          break;
       printf("Customer with ticketno %d is served\n",eventcount);
       sem_post(&m2); // releasing m2

    }

}

int main()
{
     pthread_t cust[5],barr;
     sem_init(&m1,0,1);
     sem_init(&m2,0,1);
     sem_init(&cust,0,1);
     int i;
     for(i=0;i<5;i++)
       pthread_create(&cust[i],NULL,customer,(void *)0); //creating threads
     pthread_create(&barr,NULL,barrista,(void *)0);
     for(i=0;i<5;i++)
       pthread_join(cust[i],NULL); //joining threads
     pthread_join(barr,NULL);
     return 0;
}

