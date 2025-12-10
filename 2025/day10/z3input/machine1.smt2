(set-logic QF_LIA)

; button press variables (non-negative integers)
(declare-const p0 Int) ; (3)
(declare-const p1 Int) ; (1,3)
(declare-const p2 Int) ; (2)
(declare-const p3 Int) ; (2,3)
(declare-const p4 Int) ; (0,2)
(declare-const p5 Int) ; (0,1)

; domains
(assert (>= p0 0))
(assert (>= p1 0))
(assert (>= p2 0))
(assert (>= p3 0))
(assert (>= p4 0))
(assert (>= p5 0))

; per-counter equalities to match joltage {3,5,4,7}
; counter 0
(assert (= (+ p4 p5) 3))
; counter 1
(assert (= (+ p1 p5) 5))
; counter 2
(assert (= (+ p2 p3 p4) 4))
; counter 3
(assert (= (+ p0 p1 p3) 7))

; objective: minimize total presses
(minimize (+ p0 p1 p2 p3 p4 p5))

(check-sat)
(get-objectives)
(get-model)
