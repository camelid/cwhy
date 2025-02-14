===================== Prompt =====================
This is my code:

File `/Users/runner/work/cwhy/cwhy/tests/c++/sfinae-ambiguous.cpp`:
```
 1 void f(void*) {}
 2 void f(char*) {}
 3 
 4 template <typename T>
 5 auto g(T t) -> decltype(f(t)) {
 6     return f(t);
 7 }
 8 
 9 int main() {
10     g(nullptr);
11 }
```


This is my error:
```
/Users/runner/work/cwhy/cwhy/tests/c++/sfinae-ambiguous.cpp:10:5: error: no matching function for call to 'g'
    g(nullptr);
    ^
/Users/runner/work/cwhy/cwhy/tests/c++/sfinae-ambiguous.cpp:5:6: note: candidate template ignored: substitution failure [with T = std::nullptr_t]: call to 'f' is ambiguous

[...]

auto g(T t) -> decltype(f(t)) {
     ^                  ~
1 error generated.
```


What's the problem?
==================================================
