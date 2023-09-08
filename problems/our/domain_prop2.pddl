(define (domain first_world)
(:requirements :typing :fluents :negative-preconditions :universal-preconditions :existential-preconditions)
(:types
	locatable int - object
	agent block item - locatable
	count position - int
	bedrock destructible-block - block
	log obsidian - item
	dirt-block grass_block-block log-block - destructible-block
)
(:predicates
	(agent-has-n-obsidian ?ag - agent ?n - count)
	(goal-achieved ?ag - agent)
	(agent-has-n-log ?ag - agent ?n - count)
	(item-present ?i - item)
	(at-x ?l - locatable ?x - position)
	(at-y ?l - locatable ?y - position)
	(at-z ?l - locatable ?z - position)
	(agent-alive ?ag - agent)
	(block-present ?b - block)
	(not-equal ?x1 - int ?x2 - int)
	(are-seq ?x1 - int ?x2 - int)
)
(:functions
	(x ?l - locatable )
	(y ?l - locatable )
	(agent-num-log ?ag - agent )
	(block-hits ?b - destructible-block )
	(agent-num-obsidian ?ag - agent )
	(z ?l - locatable )
)

(:action move-north
	:parameters (?ag - agent ?x - position ?y_up - position ?y_down - position ?z_start - position ?z_end - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_end ?z_start)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z_end)
))) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (at-y ?i ?y_down)
 (at-z ?i ?z_end)
))))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
)
)


(:action jumpup-north
	:parameters (?ag - agent ?x - position ?y_up - position ?y_up_up - position ?y_down - position ?z_start - position ?z_end - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_end ?z_start)
 (are-seq ?y_down ?y_up)
 (are-seq ?y_up ?y_up_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_up_up)
) (at-z ?b ?z_end)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (at-y ?b ?y_down)
 (at-z ?b ?z_end)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (or (at-y ?i ?y_down)
 (at-y ?i ?y_up)
) (at-z ?i ?z_end)
))))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_up)
)
)


(:action jumpdown-north
	:parameters (?ag - agent ?x - position ?y_up - position ?y_down - position ?y_2_down - position ?y_3_down - position ?z_start - position ?z_end - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_end ?z_start)
 (are-seq ?y_3_down ?y_2_down)
 (are-seq ?y_2_down ?y_down)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
 (at-y ?b ?y_2_down)
) (at-z ?b ?z_end)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (at-y ?b ?y_3_down)
 (at-z ?b ?z_end)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (or (at-y ?i ?y_2_down)
) (at-z ?i ?z_end)
))))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_2_down)
)
)


(:action move-south
	:parameters (?ag - agent ?x - position ?y_up - position ?y_down - position ?z_start - position ?z_end - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_start ?z_end)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z_end)
))) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (at-y ?i ?y_down)
 (at-z ?i ?z_end)
))))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
)
)


(:action jumpup-south
	:parameters (?ag - agent ?x - position ?y_up - position ?y_up_up - position ?y_down - position ?z_start - position ?z_end - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_start ?z_end)
 (are-seq ?y_down ?y_up)
 (are-seq ?y_up ?y_up_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_up_up)
) (at-z ?b ?z_end)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (at-y ?b ?y_down)
 (at-z ?b ?z_end)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (or (at-y ?i ?y_down)
 (at-y ?i ?y_up)
) (at-z ?i ?z_end)
))))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_up)
)
)


(:action jumpdown-south
	:parameters (?ag - agent ?x - position ?y_up - position ?y_down - position ?y_2_down - position ?y_3_down - position ?z_start - position ?z_end - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_start ?z_end)
 (are-seq ?y_3_down ?y_2_down)
 (are-seq ?y_2_down ?y_down)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
 (at-y ?b ?y_2_down)
) (at-z ?b ?z_end)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (at-y ?b ?y_3_down)
 (at-z ?b ?z_end)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (or (at-y ?i ?y_2_down)
) (at-z ?i ?z_end)
))))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_2_down)
)
)


(:action move-east
	:parameters (?ag - agent ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_start ?x_end)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z)
))) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (at-y ?i ?y_down)
 (at-z ?i ?z)
))))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
)
)


(:action jumpup-east
	:parameters (?ag - agent ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_up_up - position ?y_down - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_start ?x_end)
 (are-seq ?y_down ?y_up)
 (are-seq ?y_up ?y_up_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_up_up)
) (at-z ?b ?z)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (at-y ?b ?y_down)
 (at-z ?b ?z)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (or (at-y ?i ?y_down)
 (at-y ?i ?y_up)
) (at-z ?i ?z)
))))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_up)
)
)


(:action jumpdown-east
	:parameters (?ag - agent ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position ?y_2_down - position ?y_3_down - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_start ?x_end)
 (are-seq ?y_3_down ?y_2_down)
 (are-seq ?y_2_down ?y_down)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
 (at-y ?b ?y_2_down)
) (at-z ?b ?z)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (at-y ?b ?y_3_down)
 (at-z ?b ?z)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (or (at-y ?i ?y_2_down)
) (at-z ?i ?z)
))))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_2_down)
)
)


(:action move-west
	:parameters (?ag - agent ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_end ?x_start)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z)
))) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (at-y ?i ?y_down)
 (at-z ?i ?z)
))))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
)
)


(:action jumpup-west
	:parameters (?ag - agent ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_up_up - position ?y_down - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_end ?x_start)
 (are-seq ?y_down ?y_up)
 (are-seq ?y_up ?y_up_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_up_up)
) (at-z ?b ?z)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (at-y ?b ?y_down)
 (at-z ?b ?z)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (or (at-y ?i ?y_down)
 (at-y ?i ?y_up)
) (at-z ?i ?z)
))))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_up)
)
)


(:action jumpdown-west
	:parameters (?ag - agent ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position ?y_2_down - position ?y_3_down - position)
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_end ?x_start)
 (are-seq ?y_3_down ?y_2_down)
 (are-seq ?y_2_down ?y_down)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
 (at-y ?b ?y_2_down)
) (at-z ?b ?z)
))) (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (at-y ?b ?y_3_down)
 (at-z ?b ?z)
)) (not (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (or (at-y ?i ?y_2_down)
) (at-z ?i ?z)
))))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (at-y ?ag ?y_down)
) (at-y ?ag ?y_2_down)
)
)


(:action move-north-and-pickup-log
	:parameters ?ag - agent ?i - log ?x - position ?y_up - position ?y_down - position ?z_start - position ?z_end - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_end ?z_start)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z_end)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (at-y ?i ?y_down)
 (at-z ?i ?z_end)
)))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (agent-has-n-log ?ag ?n_start)
) (not (at-x ?i ?x)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z_end)
) (agent-has-n-log ?ag ?n_end)
 (not (item-present ?i)))
)


(:action move-south-and-pickup-log
	:parameters ?ag - agent ?i - log ?x - position ?y_up - position ?y_down - position ?z_start - position ?z_end - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_start ?z_end)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z_end)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (at-y ?i ?y_down)
 (at-z ?i ?z_end)
)))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (agent-has-n-log ?ag ?n_start)
) (not (at-x ?i ?x)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z_end)
) (agent-has-n-log ?ag ?n_end)
 (not (item-present ?i)))
)


(:action move-east-and-pickup-log
	:parameters ?ag - agent ?i - log ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_start ?x_end)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (at-y ?i ?y_down)
 (at-z ?i ?z)
)))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (agent-has-n-log ?ag ?n_start)
) (not (at-x ?i ?x_end)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z)
) (agent-has-n-log ?ag ?n_end)
 (not (item-present ?i)))
)


(:action move-west-and-pickup-log
	:parameters ?ag - agent ?i - log ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_end ?x_start)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (at-y ?i ?y_down)
 (at-z ?i ?z)
)))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (agent-has-n-log ?ag ?n_start)
) (not (at-x ?i ?x_end)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z)
) (agent-has-n-log ?ag ?n_end)
 (not (item-present ?i)))
)


(:action move-north-and-pickup-obsidian
	:parameters ?ag - agent ?i - obsidian ?x - position ?y_up - position ?y_down - position ?z_start - position ?z_end - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_end ?z_start)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z_end)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (at-y ?i ?y_down)
 (at-z ?i ?z_end)
)))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (agent-has-n-obsidian ?ag ?n_start)
) (not (at-x ?i ?x)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z_end)
) (agent-has-n-obsidian ?ag ?n_end)
 (not (item-present ?i)))
)


(:action move-south-and-pickup-obsidian
	:parameters ?ag - agent ?i - obsidian ?x - position ?y_up - position ?y_down - position ?z_start - position ?z_end - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z_start)
 (are-seq ?z_start ?z_end)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z_end)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x)
 (at-y ?i ?y_down)
 (at-z ?i ?z_end)
)))
	:effect (and 
(not (at-z ?ag ?z_start)
) (at-z ?ag ?z_end)
 (not (agent-has-n-obsidian ?ag ?n_start)
) (not (at-x ?i ?x)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z_end)
) (agent-has-n-obsidian ?ag ?n_end)
 (not (item-present ?i)))
)


(:action move-east-and-pickup-obsidian
	:parameters ?ag - agent ?i - obsidian ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_start ?x_end)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (at-y ?i ?y_down)
 (at-z ?i ?z)
)))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (agent-has-n-obsidian ?ag ?n_start)
) (not (at-x ?i ?x_end)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z)
) (agent-has-n-obsidian ?ag ?n_end)
 (not (item-present ?i)))
)


(:action move-west-and-pickup-obsidian
	:parameters ?ag - agent ?i - obsidian ?z - position ?x_start - position ?x_end - position ?y_up - position ?y_down - position ?n_start - count ?n_end - count
	:precondition (and 
(agent-alive ?ag)
 (at-x ?ag ?x_start)
 (at-y ?ag ?y_down)
 (at-z ?ag ?z)
 (are-seq ?x_end ?x_start)
 (are-seq ?y_down ?y_up)
 (not (exists (?b - block) (and 
(block-present ?b)
 (at-x ?b ?x_end)
 (or (at-y ?b ?y_up)
 (at-y ?b ?y_down)
) (at-z ?b ?z)
))) (exists (?i - item) (and 
(item-present ?i)
 (at-x ?i ?x_end)
 (at-y ?i ?y_down)
 (at-z ?i ?z)
)))
	:effect (and 
(not (at-x ?ag ?x_start)
) (at-x ?ag ?x_end)
 (not (agent-has-n-obsidian ?ag ?n_start)
) (not (at-x ?i ?x_end)
) (not (at-y ?i ?y_down)
) (not (at-z ?i ?z)
) (agent-has-n-obsidian ?ag ?n_end)
 (not (item-present ?i)))
)


(:action check-goal
	:parameters (?ag - agent)
	:precondition (and 
(exists (?b - log-block) (and 
(at-x ?b 0)
 (at-y ?b 4)
 (at-z ?b -2)
))
	 (or (agent-has-n-log ?ag count1)
 (agent-has-n-log ?ag count2)
 (agent-has-n-log ?ag count3)
 (agent-has-n-log ?ag count4)
 (agent-has-n-log ?ag count5)
 (agent-has-n-log ?ag count6)
 (agent-has-n-log ?ag count7)
 (agent-has-n-log ?ag count8)
 (agent-has-n-log ?ag count9)
 (agent-has-n-log ?ag count10)
 (agent-has-n-log ?ag count11)
 (agent-has-n-log ?ag count12)
 (agent-has-n-log ?ag count13)
 (agent-has-n-log ?ag count14)
 (agent-has-n-log ?ag count15)
 (agent-has-n-log ?ag count16)
 (agent-has-n-log ?ag count17)
 (agent-has-n-log ?ag count18)
 (agent-has-n-log ?ag count19)
 (agent-has-n-log ?ag count20)
 (agent-has-n-log ?ag count21)
 (agent-has-n-log ?ag count22)
 (agent-has-n-log ?ag count23)
 (agent-has-n-log ?ag count24)
 (agent-has-n-log ?ag count25)
 (agent-has-n-log ?ag count26)
 (agent-has-n-log ?ag count27)
 (agent-has-n-log ?ag count28)
 (agent-has-n-log ?ag count29)
 (agent-has-n-log ?ag count30)
 (agent-has-n-log ?ag count31)
 (agent-has-n-log ?ag count32)
 (agent-has-n-log ?ag count33)
 (agent-has-n-log ?ag count34)
 (agent-has-n-log ?ag count35)
 (agent-has-n-log ?ag count36)
 (agent-has-n-log ?ag count37)
 (agent-has-n-log ?ag count38)
 (agent-has-n-log ?ag count39)
 (agent-has-n-log ?ag count40)
 (agent-has-n-log ?ag count41)
 (agent-has-n-log ?ag count42)
 (agent-has-n-log ?ag count43)
 (agent-has-n-log ?ag count44)
 (agent-has-n-log ?ag count45)
 (agent-has-n-log ?ag count46)
 (agent-has-n-log ?ag count47)
 (agent-has-n-log ?ag count48)
 (agent-has-n-log ?ag count49)
 (agent-has-n-log ?ag count50)
 (agent-has-n-log ?ag count51)
 (agent-has-n-log ?ag count52)
 (agent-has-n-log ?ag count53)
 (agent-has-n-log ?ag count54)
 (agent-has-n-log ?ag count55)
 (agent-has-n-log ?ag count56)
 (agent-has-n-log ?ag count57)
 (agent-has-n-log ?ag count58)
 (agent-has-n-log ?ag count59)
 (agent-has-n-log ?ag count60)
 (agent-has-n-log ?ag count61)
 (agent-has-n-log ?ag count62)
 (agent-has-n-log ?ag count63)
))
	:effect (and 
(goal-achieved ?ag))
)


)