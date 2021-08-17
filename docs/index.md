# 3301Docs

This is a placeholder page.

Lorem ipsum[^1] dolor sit amet, consectetur adipiscing elit.[^2]

## Heading 1

A short code block.

```text

\[
\frac{d}{d \alpha} \int_a^b f(x, \alpha) \,dx = \int_a^b \frac{\partial f}{\partial \alpha}(x, \alpha) \,dx
\]

```

\[
\frac{d}{d \alpha} \int_a^b f(x, \alpha) \,dx = \int_a^b \frac{\partial f}{\partial \alpha}(x, \alpha) \,dx
\]

A longer code block with syntax highlighting and line numbers.

```c linenums="1"

#include <stdio.h>

int extended_euclidian(int a, int b, int *x, int *y)
{
    if (a == 0)
    {
        *x = 0;
        *y = 1;
        return b;
    }
 
    int x1, y1;
    int gcd = gcdExtended(b%a, a, &x1, &y1);

    *x = y1 - (b/a) * x1;
    *y = x1;
 
    return gcd;
}
 
int main()
{
    int x, y;
    int a = 35, b = 15;
    int g = extended_euclidian(a, b, &x, &y);
    printf("gcd(%d, %d) = %d", a, b, g);
    return 0;
}

```

## Heading 2

++ctrl+alt+del++

[^1]: Test 1.
[^2]:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

--8<-- "inclusions/abbreviations.md"
