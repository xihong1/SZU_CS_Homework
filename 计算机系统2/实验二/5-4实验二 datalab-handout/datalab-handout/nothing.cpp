#include<iostream>
#include<bitset>
using namespace std;
int allOddBits(int x)
{
    int mask=0xAA;
    mask=(mask<<8)|mask;
    mask=(mask<<16)|mask;
    cout<<bitset<32>(mask)<<endl;
    cout<<bitset<32>(x)<<endl;
    cout<<bitset<32>((x&mask))<<endl;
    cout<<bitset<32>((x&mask)^mask)<<endl;
    cout<<bitset<32>(!((x&mask)^mask))<<endl;
    return !((x&mask)^mask);
}
int main()
{
    cout<<allOddBits(0xAAAAAAAA)<<endl;
    cout<<allOddBits(0xFFFFFFFE)<<endl;
    cout<<allOddBits(0x55555555)<<endl;
    cout<<allOddBits(0xFFFFFFFF)<<endl;
    return 0;
}