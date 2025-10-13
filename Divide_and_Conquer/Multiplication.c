#include <stdio.h>
#include <stdlib.h>

#define max 30
/*
    几个计算乘法的问题, 通过分治提升效率.
    问题一: 大整数乘法
        问题描述:两个 n 位整数 X, Y, 计算 X*Y
        如果按照列竖式的方法, 每一位拆开计算, 则需要 O(n^2)复杂度
        为了降低复杂度, 采用分治算法
        在分治算法中进行优化, 能够进一步降低时间复杂度, 约为 O(n^(log_2^(3))) (Karatsuba算法)
        具体参考 PPT: Week04_Lecture08_Polynomial Multiplication_250929.pdf

    问题二: 多项式乘法
        问题描述: 两个 n 次实多项式 A(x), B(x), 计算 C(x)=A(x)B(x)
        A(x), B(x)均通过数组形式存储.
        如, A(x)系数存储在 coeA[]中, coeA[i]表示 x^i 的系数(i=0, 1, 2, ...n)

        传统算法: 
            A(x) 和 B(x) 通过乘法分配律展开相乘相加
            乘法运算 n^2次, 加法运算 n^2-1 次, 时间复杂度 O(n^2)
        
        通过分治算法进行计算:
            将 A(x)和 B(x)拆分:
                A(x)=C(x)*x^(n/2)+D(x)
                B(x)=E(x)*x^(n/2)+F(x)
            然后计算子问题 C(x)*E(x), C(x)*F(x), D(x)*E(x), D(x)*F(x), 根据对应的 x幂次合并出最终结果
            此时的复杂度:T(n)=4*T(n/2)+O(n) (根据对应幂次合并相加, 复杂度 O(n))
            A(x)*B(x)=C(x)*E(x)*x^n+(C(x)*F(x)+D(x)*E(x))*x^(n/2)+D(x)*F(x) (*)

            根据主定理, 算出 T(n)=O(n^2), 和传统算法相比没有提升!
            
            优化: 根据主定理, T(n)=a*T(n/b)+f(n), 此处 f(n)=O(n), 如果能减少 a 的值, 即减少分治产生的子问题数量, 可以降低复杂度
            如何减少子问题计算数量? -- 通过已知量表示未知量!
            令:
            U(x)=C(x)*E(x)
            V(x)=D(x)*F(x)
            Y(x)=(C(x)+D(x))*(E(x)+F(x))
            则: (*)式中间项(C(x)*F(x)+D(x)*E(x))=Y(x)-U(x)-V(x), 无需通过C(x)*F(x), D(x)*E(x)两个子问题分别计算出!
            此时, 子问题为 3 个--U, V, Y.

            T(n)=3*T(n/2)+O(n)
            根据主定理, T(n)=O(n^(log_2^(3)))≈O(1.58)


    问题三: 矩阵乘法
        问题描述: 两个 n 阶实方阵 A,B, 计算 C=A*B
        传统方法:
            按照定义求, C 的每个元素需要经过n 次乘法和 n-1 次加法, O(2n-1)=O(n)
            C 中共有 n^2 个元素, 因此复杂度 O(n^3)
        
        通过分治算法进行计算:
            思路同上, 将矩阵 A 和 B 各分为 4 块, 进行计算求和, 降低复杂度

            优化:为了进一步精简, 减少计算的子问题的数量, 可以利用已知量表示未知量, 从而达到O(n^(log_2^(7)))的时间复杂度
            (Strassen 算法, 具体见PPT: Week04_Lecture08_Polynomial Multiplication_250929.pdf)
*/

int* Polynomial(int* coeA, int* coeB, int n) // 常规做法
{
    int* ans=(int*)calloc(2*n+1, sizeof(int));
    for(int i=0; i<=n; i++)
        for(int j=0; j<=n; j++)
            ans[i+j]+=coeA[i]*coeB[j];
    return ans;
}


int* Polynomial_Add(int* coeA, int nA, int* coeB, int nB)
{
    // 实现两个多项式系数相加, 求和多项式
    // 默认 nA>nB
    if(nA<nB)
        return Polynomial_Add(coeB, nB, coeA, nA);
    int* ans=(int*)calloc(nA+1, sizeof(int));
    for(int i=0; i<=nA; i++)
        ans[i]=(i<=nB)?(coeA[i]+coeB[i]):(coeA[i]);
    return ans;
}

void Polynomial_Split(int* coe, int n, int** coe_low, int** coe_high, int* n_low, int* n_high)
{
    // 将一个 n 次多项式拆分成次数为 0~n/2-1 和 n/2~n 的部分
    int mid=n/2;
    *coe_low=(int*)calloc(mid, sizeof(int));
    *n_low=mid-1;

    *coe_high=(int*)calloc(n-mid+1, sizeof(int));
    *n_high=n-mid;

    for(int i=0; i<=n; i++)
    {
        if(i<mid)
            (*coe_low)[i]=coe[i];
        else
            (*coe_high)[i-mid]=coe[i];
    }
}


int* Divide_and_Conquer(int* coeA, int* coeB, int n)
{
    int* ans=(int*)calloc(2*n+1, sizeof(int));
    if(n==0)
    {
        ans[0]=coeA[0]*coeB[0];
        return ans;
    }
    else // n>0
    {
        int *coeA_low=NULL, *coeA_high=NULL;
        int *coeB_low=NULL, *coeB_high=NULL;
        int n_low=-1, n_high=-1;

        Polynomial_Split(coeA, n, &coeA_low, &coeA_high, &n_low, &n_high);
        Polynomial_Split(coeB, n, &coeB_low, &coeB_high, &n_low, &n_high);
  
        int* U=Divide_and_Conquer(coeA_low, coeB_low, n_low);
        int* V=Divide_and_Conquer(coeA_high, coeB_high, n_high);
        
        int* Aplus=Polynomial_Add(coeA_low, n_low, coeA_high, n_high);
        int* Bplus=Polynomial_Add(coeB_low, n_low, coeB_high, n_high);
        int n_max=(n_low>n_high)?n_low:n_high;

        int* Y=Divide_and_Conquer(Aplus, Bplus, n_max);
        // 做减法Y-U-V, 求出中间项C(x)*F(x)+D(x)*E(x)
        // 搞清楚每一个多项式次数都是多少, 然后再进行计算
        // A(x)*B(x)=C(x)*E(x)*x^n+(C(x)*F(x)+D(x)*E(x))*x^(n/2)+D(x)*F(x)
    }
}

int* Polynomial_Divide_and_Conquer(int* coeA, int* coeB, int n)
{
    return Divide_and_Conquer(coeA, coeB, n);
}



/*----------------------Test Case----------------------*/
int main()
{
    int coeA[]={1, 2, 3, -2, 1};
    int coeB[]={-1, 3, 4, 7, 9};
    int n=sizeof(coeA)/sizeof(int)-1;

    // 常规做法
    int* ans_method1=Polynomial(coeA, coeB, n);
    for(int i=0; i<=2*n; i++)
        printf("%+d*(x^%d)", ans_method1[i], i); 
    printf("\n");
    // %+d 是 C 语言 printf 格式化输出中的一种格式控制符，作用是在输出整数时强制显示正负号
 
    int* ans_method2=Polynomial_Divide_and_Conquer(coeA, coeB, n);
    for(int i=0; i<=2*n; i++)
        printf("%+d*(x^%d)", ans_method2[i], i);
    printf("\n"); 

    // int* ans=Polynomial_Add(coeA, n, coeB, n);
    // for(int i=0; i<=n; i++)
    //     printf("%+d*(x^%d)", ans[i], i); 
    // printf("\n");

    // int* coe_low=NULL;
    // int* coe_high=NULL;
    // int n_low=-1;
    // int n_high=-1;
    // Polynomial_Split(coeB, n, &coe_low, &coe_high, &n_low, &n_high);

    // for(int i=0; i<=n_low; i++)
    //     printf("%d ", coe_low[i]);
    // printf("\n");   
    // for(int i=0; i<=n_high; i++)
    //     printf("%d ", coe_high[i]);
    // printf("\n");  
}

