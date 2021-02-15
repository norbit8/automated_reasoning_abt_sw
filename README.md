![67532 AUTOMATED REASONING ABOUT SOFTWARE](https://github.com/norbit8/automated_reasoning_abt_sw/blob/main/logo.png?raw=true)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
![python versions](https://img.shields.io/pypi/pyversions/firebase?style=flat-square)
<space>
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## SAT Solver
In order to use the SAT solver, you'll need to import `sat_solver.sat_engine` and then calling the function `solve_sat(formula)` where 
a formula is defined like so
- An atomic proposition should be a letter in 'p' ... 'z', optionally followed by a sequence of digits. Examples: 'p', 'y12', 'z035'.

- Could have 'T' and 'F' (as True and False respectively).

- ~φ where φ is a valid propositional formula.

- '(φ&ψ)' where each of φ and ψ is a valid propositional formula.

- '(φ|ψ)' where each of φ and ψ is a valid propositional formula.

- '(φ->ψ)' where each of φ and ψ is a valid propositional formula.

Example:
  ```
  from sat_solver.sat_engine import *
  formula = Formula('(~p0|~pq<->(p2<->(p3->p4))))')
  print(solve_sat(formula))
  ```
## SMT Solver
bla bla

## LP Solver
bla bla

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/shaigindin"><img src="https://avatars.githubusercontent.com/u/49125116?v=4?s=100" width="100px;" alt=""/><br /><sub><b>shaigindin</b></sub></a><br /><a href="#infra-shaigindin" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/norbit8/automated_reasoning_abt_sw/commits?author=shaigindin" title="Tests">⚠️</a> <a href="https://github.com/norbit8/automated_reasoning_abt_sw/commits?author=shaigindin" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/norbit8"><img src="https://avatars.githubusercontent.com/u/18491183?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Yoav</b></sub></a><br /><a href="#infra-norbit8" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/norbit8/automated_reasoning_abt_sw/commits?author=norbit8" title="Tests">⚠️</a> <a href="https://github.com/norbit8/automated_reasoning_abt_sw/commits?author=norbit8" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
