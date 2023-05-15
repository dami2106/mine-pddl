(define (domain first_world)
(:requirements :typing  :negative-preconditions :universal-preconditions :existential-preconditions)
(:types
	locatable - object
	agent block item - locatable
	bedrock destructible-block - block
	oak-log diamond_axe diamond - item
	stone dirt grass_block leaves grass obsidian coal_ore - destructible-block
)
(:predicates
	(block-present ?b - block)
	(item-present ?i - item)
	(agent-alive ?ag - agent)
)
(:functions
	(y ?l - locatable )
	(x ?l - locatable )
	(z ?l - locatable )
	(block-hits ?b - destructible-block )
	(agent-num-diamond ?ag - agent )
	(agent-num-diamond_axe ?ag - agent )
	(agent-num-oak-log ?ag - agent )
)

(:action move-north
	:parameters (?ag - agent)
	:precondition (and (agent-alive ?ag) (not (exists (?b - block) (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1))))))
	:effect (and (decrease (z ?ag) 1))
)


(:action move-south
	:parameters (?ag - agent)
	:precondition (and (agent-alive ?ag) (not (exists (?b - block) (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) 1))))))
	:effect (and (increase (z ?ag) 1))
)


(:action move-east
	:parameters (?ag - agent)
	:precondition (and (agent-alive ?ag) (not (exists (?b - block) (and (= (x ?b) (+ (x ?ag) 1)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (z ?ag))))))
	:effect (and (increase (x ?ag) 1))
)


(:action move-west
	:parameters (?ag - agent)
	:precondition (and (agent-alive ?ag) (not (exists (?b - block) (and (= (x ?b) (+ (x ?ag) -1)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (z ?ag))))))
	:effect (and (decrease (x ?ag) 1))
)


(:action pickup-oak-log
	:parameters (?ag - agent ?i - oak-log)
	:precondition (and (item-present ?i) (= (x ?i) (x ?ag)) (= (y ?i) (y ?ag)) (= (z ?i) (z ?ag)))
	:effect (and (increase (agent-num-oak-log ?ag) 1) (not (item-present ?i)))
)


(:action drop-oak-log
	:parameters (?ag - agent ?i - oak-log)
	:precondition (and (>= (agent-num-oak-log ?ag) 1) (not (item-present ?i)))
	:effect (and (item-present ?i) (assign (x ?i) (x ?ag)) (assign (y ?i) (y ?ag)) (assign (z ?i) (+ (z ?ag) -1)) (decrease (agent-num-oak-log ?ag) 1))
)


(:action pickup-diamond_axe
	:parameters (?ag - agent ?i - diamond_axe)
	:precondition (and (item-present ?i) (= (x ?i) (x ?ag)) (= (y ?i) (y ?ag)) (= (z ?i) (z ?ag)))
	:effect (and (increase (agent-num-diamond_axe ?ag) 1) (not (item-present ?i)))
)


(:action drop-diamond_axe
	:parameters (?ag - agent ?i - diamond_axe)
	:precondition (and (>= (agent-num-diamond_axe ?ag) 1) (not (item-present ?i)))
	:effect (and (item-present ?i) (assign (x ?i) (x ?ag)) (assign (y ?i) (y ?ag)) (assign (z ?i) (+ (z ?ag) -1)) (decrease (agent-num-diamond_axe ?ag) 1))
)


(:action pickup-diamond
	:parameters (?ag - agent ?i - diamond)
	:precondition (and (item-present ?i) (= (x ?i) (x ?ag)) (= (y ?i) (y ?ag)) (= (z ?i) (z ?ag)))
	:effect (and (increase (agent-num-diamond ?ag) 1) (not (item-present ?i)))
)


(:action drop-diamond
	:parameters (?ag - agent ?i - diamond)
	:precondition (and (>= (agent-num-diamond ?ag) 1) (not (item-present ?i)))
	:effect (and (item-present ?i) (assign (x ?i) (x ?ag)) (assign (y ?i) (y ?ag)) (assign (z ?i) (+ (z ?ag) -1)) (decrease (agent-num-diamond ?ag) 1))
)
)

	