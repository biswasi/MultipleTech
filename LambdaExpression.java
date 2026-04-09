import java.io.*;
import java.util.*;

/*Write the following methods that return a lambda expression performing a specified action:
PerformOperation isOdd(): The lambda expression must return  if a number is odd or  if it is even.
PerformOperation isPrime(): The lambda expression must return  if a number is prime or  if it is composite.
PerformOperation isPalindrome(): The lambda expression must return  if a number is a palindrome or  if it is not.*/

public class Solution {

public static void main(String[] args) {
   /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
    
    Scanner scan = new Scanner(System.in);
    int full = scan.nextInt();
    while(full--> 0){
        int code = scan.nextInt();
        int number = scan.nextInt();
        if (code==1){
            boolean a = executeOperation(n-> isOdd(n), number);
        System.out.println(a==true?"EVEN":"ODD");
        }else if(code==2){
               boolean a = executeOperation(n-> isPrime(n), number);
        System.out.println(a==true?"PRIME":"COMPOSITE");
        }else{
               boolean a = executeOperation(n-> isPalindrome(n), number);
        System.out.println(a==true?"PALINDROME":"NOT PALINDROME");
        }
    }
}
@FunctionalInterface
 interface Predicate<T>{
    boolean test(int a);
     }
static boolean executeOperation(Predicate<Integer> predi, int number) {
    return predi.test(number);

}
static boolean isPrime(int number) {
    for(int i=2;i<(int)Math.sqrt(number);i++){
        if(number%i==0) return false;
    }
    return true;
}
static boolean isPalindrome(int number) {
    String c = ""+number;
    StringBuilder b = new StringBuilder(c).reverse();
    int d = Integer.parseInt(b.toString());
    return number==d;
}

static boolean isOdd(int number) {
    return number%2==0;
}
}
