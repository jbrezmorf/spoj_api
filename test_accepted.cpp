#include <iostream>

int main() {
  int i=0;
  while (1) {
      std::cin >> i;
      if (i==42) return 0;
      else std::cout << i << std::endl;
  }
}  
      
  