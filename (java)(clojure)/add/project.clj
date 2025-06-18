(defproject add "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :dependencies [[org.clojure/clojure "1.11.1"]]
  :main add.core
  :aot [add.core]
  :target-path "target/%s"
		:profiles {:uberjar {:aot :all}})