int avg();
int incr(); 
int count1=0;
int count2=0;
int pr[10],fa[10];
int main(int argc, char const *argv[])
{
int input,i; 
float av1,av2;
for(i=1;i<=10;i++)
    {
        do
            {
            printf("Enter grade no.%d : \n",i);
            scanf("%d",&input);
            
            }
        while((input<0 && input!=-1)|| input>10);
    if(input==-1)
            {
                break;
            }
    if(input>=5)
    {
        pr[count1]=input;
        count1++;
    }
    else if(input<=10)
    {
        fa[count2]=input;
        count2++
        
    }

    }
avg(pr,fa);
if(count2>count1)
{
    incr(pr,fa);
    avg(pr,fa);
}
return 0;
}
int avg(){
    float sum1=0;
    float sum2=0;
    int i=0;
    while(i!=count1)
    {
        sum1+=pr[i];
        i++;
    }
    sum1=sum1/count1;
    i=0;
    while(i!=count2)
    {
        sum2+=fa[i];
        i++;
    }
    sum2=sum2/count2;
    printf("Passed :average score:%f\n",sum1);
    printf("Failed :average score:%f\n",sum2);
    return 0;}

int incr()
{
    int i=0;
    printf("%d\t%d",count1,count2);
    while(fa[i]==4)
    {   fa[i]++;
        count1++;
        count2--;
        i++;
        if(count2>count1)
        {
            break;
        }
    }
    printf("%d\t%d",count1,count2);
    return 0;
}