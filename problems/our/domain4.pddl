(define (domain first_world)
(:requirements :typing :fluents :negative-preconditions :universal-preconditions :existential-preconditions)
(:types
	locatable - object
	agent block item - locatable
	bedrock destructible-block - block
	oak-log log - item
	dirt grass_block obsidian wood - destructible-block
)
(:predicates
	(item-present ?i - item)
	(agent-alive ?ag - agent)
	(block-present ?b - block)
)
(:functions
	(agent-num-log ?ag - agent )
	(agent-num-oak-log ?ag - agent )
	(z ?l - locatable )
	(x ?l - locatable )
	(block-hits ?b - destructible-block )
	(y ?l - locatable )
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


(:action pickup-log
	:parameters (?ag - agent ?i - log)
	:precondition (and (item-present ?i) (= (x ?i) (x ?ag)) (= (y ?i) (y ?ag)) (= (z ?i) (z ?ag)))
	:effect (and (increase (agent-num-log ?ag) 1) (not (item-present ?i)))
)


(:action drop-log
	:parameters (?ag - agent ?i - log)
	:precondition (and (>= (agent-num-log ?ag) 1) (not (item-present ?i)))
	:effect (and (item-present ?i) (assign (x ?i) (x ?ag)) (assign (y ?i) (y ?ag)) (assign (z ?i) (+ (z ?ag) -1)) (decrease (agent-num-log ?ag) 1))
)


(:action break-dirt
	:parameters (?ag - agent ?b - dirt)
	:precondition (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1)) (block-present ?b))
	:effect (and (not (block-present ?b)) (increase (agent-num-dirt ?ag) 1))
)


(:action place-dirt
	:parameters (?ag - agent ?b - dirt)
	:precondition (and (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (+ (y ?bl) 1)) (= (z ?b) (z ?bl)))) (not (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (y ?bl)) (= (z ?b) (z ?bl))))) (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1))))
	:effect (and (block-present ?b) (assign (x ?b) (x ?ag)) (assign (y ?b) (+ (y ?ag) 1)) (assign (z ?b) (+ (z ?ag) -1)) (decrease (agent-num-dirt ?ag) 1))
)


(:action break-grass_block
	:parameters (?ag - agent ?b - grass_block)
	:precondition (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1)) (block-present ?b))
	:effect (and (not (block-present ?b)) (increase (agent-num-grass_block ?ag) 1))
)


(:action place-grass_block
	:parameters (?ag - agent ?b - grass_block)
	:precondition (and (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (+ (y ?bl) 1)) (= (z ?b) (z ?bl)))) (not (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (y ?bl)) (= (z ?b) (z ?bl))))) (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1))))
	:effect (and (block-present ?b) (assign (x ?b) (x ?ag)) (assign (y ?b) (+ (y ?ag) 1)) (assign (z ?b) (+ (z ?ag) -1)) (decrease (agent-num-grass_block ?ag) 1))
)


(:action break-obsidian
	:parameters (?ag - agent ?b - obsidian)
	:precondition (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1)) (block-present ?b))
	:effect (and (not (block-present ?b)) (increase (agent-num-obsidian ?ag) 1))
)


(:action place-obsidian
	:parameters (?ag - agent ?b - obsidian)
	:precondition (and (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (+ (y ?bl) 1)) (= (z ?b) (z ?bl)))) (not (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (y ?bl)) (= (z ?b) (z ?bl))))) (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1))))
	:effect (and (block-present ?b) (assign (x ?b) (x ?ag)) (assign (y ?b) (+ (y ?ag) 1)) (assign (z ?b) (+ (z ?ag) -1)) (decrease (agent-num-obsidian ?ag) 1))
)


(:action break-wood
	:parameters (?ag - agent ?b - wood)
	:precondition (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1)) (block-present ?b))
	:effect (and (not (block-present ?b)) (increase (agent-num-wood ?ag) 1))
)


(:action place-wood
	:parameters (?ag - agent ?b - wood)
	:precondition (and (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (+ (y ?bl) 1)) (= (z ?b) (z ?bl)))) (not (exists (?bl - block) (and (= (x ?b) (x ?bl)) (= (y ?b) (y ?bl)) (= (z ?b) (z ?bl))))) (and (= (x ?b) (x ?ag)) (= (y ?b) (+ (y ?ag) 1)) (= (z ?b) (+ (z ?ag) -1))))
	:effect (and (block-present ?b) (assign (x ?b) (x ?ag)) (assign (y ?b) (+ (y ?ag) 1)) (assign (z ?b) (+ (z ?ag) -1)) (decrease (agent-num-wood ?ag) 1))
)


(:action jump-up
	:parameters (?ag - agent)
	:precondition (and (exists (?bl - block) (and (= (x ?bl) (x ?ag)) (= (y ?bl) (y ?ag)) (= (z ?bl) (+ (z ?ag) 1)))))
	:effect (and (assign (z ?ag) (+ (z ?ag) -1)) (assign (y ?ag) (+ (y ?ag) 1)))
)


)