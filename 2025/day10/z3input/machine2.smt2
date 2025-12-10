(set-logic QF_LIA)

; button press variables (non-negative integers)
(declare-const p0 Int) ; (0,2,3,4)
(declare-const p1 Int) ; (2,3)
(declare-const p2 Int) ; (0,4)
(declare-const p3 Int) ; (0,1,2)
(declare-const p4 Int) ; (1,2,3,4)

; domains
(assert (>= p0 0))
(assert (>= p1 0))
(assert (>= p2 0))
(assert (>= p3 0))
(assert (>= p4 0))

; per-counter equalities to match joltage {7,5,12,7,2}
; counter 0
(assert (= (+ p0 p2 p3) 7))
; counter 1
(assert (= (+ p3 p4) 5))
; counter 2
(assert (= (+ p0 p1 p3 p4) 12))
; counter 3
(assert (= (+ p0 p1 p4) 7))
; counter 4
(assert (= (+ p0 p2 p4) 2))

; objective: minimize total presses
(minimize (+ p0 p1 p2 p3 p4))

(check-sat)
(get-objectives)
(get-model)
