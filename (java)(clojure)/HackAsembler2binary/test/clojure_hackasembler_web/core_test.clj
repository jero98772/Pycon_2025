(ns clojure-hackasembler-web.core-test
  (:require [clojure.test :refer :all]
            [clojure-hackasembler-web.core :refer :all]))

(deftest test-clean-line
  (testing "clean-line function"
    (is (= "D=A" (clean-line "D=A // comment")))
    (is (= "D=A" (clean-line "  D=A  ")))
    (is (= "" (clean-line "// just a comment")))
    (is (= "" (clean-line "   ")))))

(deftest test-label?
  (testing "label? function"
    (is (true? (label? "(LOOP)")))
    (is (true? (label? "(END)")))
    (is (false? (label? "D=A")))
    (is (false? (label? "@123")))))

(deftest test-numeric?
  (testing "numeric? function"
    (is (true? (numeric? "123")))
    (is (true? (numeric? "0")))
    (is (false? (numeric? "abc")))
    (is (false? (numeric? "R1")))))

(deftest test-parse-c-instruction
  (testing "parse-c-instruction function"
    (is (= ["D" "A" ""] (parse-c-instruction "D=A")))
    (is (= ["" "D" "JMP"] (parse-c-instruction "D;JMP")))
    (is (= ["MD" "D+1" "JGT"] (parse-c-instruction "MD=D+1;JGT")))
    (is (= ["" "0" ""] (parse-c-instruction "0")))))

(deftest test-translate-a-instruction
  (testing "translate-a-instruction function"
    (let [symbol-table {"R0" 0, "LOOP" 10}
          next-var-addr 16]
      ; Test numeric address
      (let [[st nva result] (translate-a-instruction "@123" symbol-table next-var-addr)]
        (is (= "000000001111011" result)))
      
      ; Test existing symbol
      (let [[st nva result] (translate-a-instruction "@R0" symbol-table next-var-addr)]
        (is (= "000000000000000" result)))
      
      ; Test new variable
      (let [[st nva result] (translate-a-instruction "@newvar" symbol-table next-var-addr)]
        (is (= "000000000010000" result))
        (is (= 17 nva))
        (is (= 16 (st "newvar")))))))

(deftest test-translate-c-instruction
  (testing "translate-c-instruction function"
    (is (= "1110110000010000" (translate-c-instruction "D=A")))
    (is (= "1110001100000111" (translate-c-instruction "D;JMP")))
    (is (= "1110101010000000" (translate-c-instruction "0")))))

(deftest test-assemble-simple
  (testing "assemble function with simple code"
    (let [code "@2\nD=A\n@0\nM=D"
          result (assemble code)
          lines (clojure.string/split-lines result)]
      (is (= 4 (count lines)))
      (is (= "0000000000000010" (first lines)))
      (is (= "1110110000010000" (second lines)))
      (is (= "0000000000000000" (nth lines 2)))
      (is (= "1110001100001000" (nth lines 3))))))

(deftest test-assemble-with-labels
  (testing "assemble function with labels"
    (let [code "(LOOP)\n@LOOP\n0;JMP"
          result (assemble code)
          lines (clojure.string/split-lines result)]
      (is (= 2 (count lines)))
      (is (= "0000000000000000" (first lines))) ; @LOOP should reference address 0
      (is (= "1110101010000111" (second lines))))))

(run-tests)