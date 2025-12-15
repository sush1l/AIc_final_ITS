def convert_fraction(n, d):
    return n / d

def step_by_step(n, d):
    steps = []
    steps.append(f"1. Identify numerator = {n} and denominator = {d}.")
    if n >= d:
        whole = n // d
        rem = n % d
        steps.append(f"2. Since numerator ≥ denominator, whole part = {whole}, remainder = {rem}.")
        if rem == 0:
            steps.append(f"3. Fraction equals the integer {whole}.")
        else:
            steps.append("3. Convert remainder by long division.")
    else:
        steps.append("2. Perform long division: numerator ÷ denominator.")
    steps.append(f"Final result: {n}/{d} = {n/d}")
    return steps

def fraction_hint(n, d):
    if d == 0:
        return "Denominator cannot be zero."

    if n % d == 0:
        return "This fraction simplifies to an integer."

    # terminating decimal?
    def prime_factors(x):
        pf = set()
        i = 2
        while i * i <= x:
            while x % i == 0:
                pf.add(i)
                x //= i
            i += 1
        if x > 1:
            pf.add(x)
        return pf

    pf = prime_factors(d)
    if pf.issubset({2, 5}):
        return "This is a terminating decimal (denominator factors only 2 & 5)."
    else:
        return "This decimal repeats (denominator has primes other than 2 & 5)."

def ontology_lookup(graph, ns, n, d):
    query = f"""
    PREFIX : <http://example.org/fractions#>
    SELECT ?decVal WHERE {{
      ?f a :Fraction .
      ?f :hasNumerator ?num .
      ?num :hasValue "{n}" .
      ?f :hasDenominator ?den .
      ?den :hasValue "{d}" .
      ?f :convertsTo ?dec .
      ?dec :hasValue ?decVal .
    }}
    """
    results = list(graph.query(query))
    if results:
        return f"Ontology: Known conversion → {results[0][0]}"
    return "Ontology: No exact match found."
