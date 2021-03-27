#include <stdio.h>
int case1(float x[2][3],int ct);
float case2(float x[2][3],int ct);
int main(int argc, char const *argv[])
{
    int i,j;
    float g1,g2;
    float *ptr1;
    float *ptr2;
    ptr1=&g1;
    ptr2=&g2;
    float grades[2][3];
    for(i=0;i<3;i++)///student 1
    {
            do
            {
                printf("Enter grade %d of student 1: ",(i+1));
                scanf("\n%f",ptr1);
            }
            while(*ptr1<0 || *ptr1>10);
            grades[0][i]=*ptr1;
    }
    for(i=0;i<3;i++)///student 2
    {
            do
            {
                printf("Enter grade %d of student 2: ",(i+1));
                scanf("\n%f",ptr2);
            }
            while(*ptr2<0 || *ptr2>10);
            grades[1][i]=*ptr2;
    }
    int ct=0;
    printf("student1: ");
    if(grades[0][0]>=5 && grades[0][1]>=5 && grades[0][2]>=5)
    {
        case1(grades,ct);
    }
    else
    {
        printf("Average: %f",case2(grades,ct));
    }
    ct++;
    printf("\nstudent2: ");
    if(grades[1][0]>5 && grades[1][1]>5 && grades[1][2]>5)
    {
        case1(grades,ct);
    }
    else
    {
        printf("Average: %f",case2(grades,ct));
    }


    if(case2(grades,0)>case2(grades,1))
    {
        printf("\nThe first student had better performance");
    }
    else
    {
        printf("\nThe second student had better performance");
    }
return 0;
}

int case1(float x[2][3],int ct)
    {
    int i;
    if(x[ct][0]<x[ct][1] && x[ct][0]>x[ct][2])
    {
        printf("%f\t%f\t%f",x[ct][2],x[ct][0],x[ct][1]);
    }
    else if(x[ct][1]<x[ct][0] && x[ct][1]>x[ct][2])
    {
        printf("%f\t%f\t%f",x[ct][2],x[ct][1],x[ct][0]);
    }
    else if(x[ct][1]<x[ct][2] && x[ct][1]>x[ct][0])
    {
        printf("%f\t%f\t%f",x[ct][0],x[ct][1],x[ct][2]);
    }
    else if(x[ct][0]<x[ct][2] && x[ct][0]>x[ct][1])
    {
        printf("%f\t%f\t%f",x[ct][1],x[ct][0],x[ct][2]);
    }
    else if(x[ct][2]<x[ct][0] && x[ct][2]>x[ct][1])
    {
        printf("%f\t%f\t%f",x[ct][0],x[ct][2],x[ct][0]);
    }
    else if(x[ct][2]<x[ct][1] && x[ct][2]>x[ct][0])
    {
        printf("%f\t%f\t%f",x[ct][0],x[ct][2],x[ct][1]);
    }
    return 0;
    }

float case2(float x[2][3],int ct)
    {
    int i;
    float sum=0;
    float wow;
    for(i=0;i<3;i++)
    {
        wow=x[ct][i];
        sum+=tmp;
    }
    sum=sum/3;
    return sum;
    }