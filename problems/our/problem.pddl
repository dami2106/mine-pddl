(define (problem first_world_problem)
	(:domain first_world)
(:objects
	steve - agent
	grass_block-block0 grass_block-block1 grass_block-block2 grass_block-block3 grass_block-block4 grass_block-block5 grass_block-block6 grass_block-block7 grass_block-block8 grass_block-block9 grass_block-block10 grass_block-block11 grass_block-block12 grass_block-block13 grass_block-block14 grass_block-block15 grass_block-block16 grass_block-block17 grass_block-block18 grass_block-block19 grass_block-block20 grass_block-block21 grass_block-block22 grass_block-block23 grass_block-block24 grass_block-block25 grass_block-block26 grass_block-block27 grass_block-block28 grass_block-block29 grass_block-block30 grass_block-block31 grass_block-block32 grass_block-block33 grass_block-block34 grass_block-block35 grass_block-block36 grass_block-block37 grass_block-block38 grass_block-block39 grass_block-block40 grass_block-block41 grass_block-block42 grass_block-block43 grass_block-block44 grass_block-block45 grass_block-block46 grass_block-block47 grass_block-block48 grass_block-block49 grass_block-block50 grass_block-block51 grass_block-block52 grass_block-block53 grass_block-block54 grass_block-block55 grass_block-block56 grass_block-block57 grass_block-block58 grass_block-block59 grass_block-block60 grass_block-block61 grass_block-block62 grass_block-block63 grass_block-block64 grass_block-block65 grass_block-block66 grass_block-block67 grass_block-block68 grass_block-block69 grass_block-block70 grass_block-block71 grass_block-block72 grass_block-block73 grass_block-block74 grass_block-block75 grass_block-block76 grass_block-block77 grass_block-block78 grass_block-block79 grass_block-block80 - grass_block-block
	obsidian-block0 - obsidian-block
	log-block0 - log-block
	diamond0 - diamond
	oak-log0 - oak-log
	log0 - log
	obsidian0 - obsidian
)
(:init
	(agent-alive steve)
	(goal-achieved steve)
	(= (x steve) 0)
	(= (y steve) 4)
	(= (z steve) 0)
	(= (agent-num-diamond steve) 0)
	(= (agent-num-oak-log steve) 0)
	(= (agent-num-log steve) 64)
	(= (agent-num-obsidian steve) 64)
	(block-present grass_block-block0)
	(= (x grass_block-block0) -3)
	(= (y grass_block-block0) 3)
	(= (z grass_block-block0) -3)
	(= (block-hits grass_block-block0) 0)
	(block-present grass_block-block1)
	(= (x grass_block-block1) -3)
	(= (y grass_block-block1) 3)
	(= (z grass_block-block1) -2)
	(= (block-hits grass_block-block1) 0)
	(block-present grass_block-block2)
	(= (x grass_block-block2) -3)
	(= (y grass_block-block2) 3)
	(= (z grass_block-block2) -1)
	(= (block-hits grass_block-block2) 0)
	(block-present grass_block-block3)
	(= (x grass_block-block3) -3)
	(= (y grass_block-block3) 3)
	(= (z grass_block-block3) 0)
	(= (block-hits grass_block-block3) 0)
	(block-present grass_block-block4)
	(= (x grass_block-block4) -3)
	(= (y grass_block-block4) 3)
	(= (z grass_block-block4) 0)
	(= (block-hits grass_block-block4) 0)
	(block-present grass_block-block5)
	(= (x grass_block-block5) -3)
	(= (y grass_block-block5) 3)
	(= (z grass_block-block5) 1)
	(= (block-hits grass_block-block5) 0)
	(block-present grass_block-block6)
	(= (x grass_block-block6) -3)
	(= (y grass_block-block6) 3)
	(= (z grass_block-block6) 2)
	(= (block-hits grass_block-block6) 0)
	(block-present grass_block-block7)
	(= (x grass_block-block7) -3)
	(= (y grass_block-block7) 3)
	(= (z grass_block-block7) 3)
	(= (block-hits grass_block-block7) 0)
	(block-present grass_block-block8)
	(= (x grass_block-block8) -3)
	(= (y grass_block-block8) 3)
	(= (z grass_block-block8) 4)
	(= (block-hits grass_block-block8) 0)
	(block-present grass_block-block9)
	(= (x grass_block-block9) -2)
	(= (y grass_block-block9) 3)
	(= (z grass_block-block9) -3)
	(= (block-hits grass_block-block9) 0)
	(block-present grass_block-block10)
	(= (x grass_block-block10) -2)
	(= (y grass_block-block10) 3)
	(= (z grass_block-block10) -2)
	(= (block-hits grass_block-block10) 0)
	(block-present grass_block-block11)
	(= (x grass_block-block11) -2)
	(= (y grass_block-block11) 3)
	(= (z grass_block-block11) -1)
	(= (block-hits grass_block-block11) 0)
	(block-present grass_block-block12)
	(= (x grass_block-block12) -2)
	(= (y grass_block-block12) 3)
	(= (z grass_block-block12) 0)
	(= (block-hits grass_block-block12) 0)
	(block-present grass_block-block13)
	(= (x grass_block-block13) -2)
	(= (y grass_block-block13) 3)
	(= (z grass_block-block13) 0)
	(= (block-hits grass_block-block13) 0)
	(block-present grass_block-block14)
	(= (x grass_block-block14) -2)
	(= (y grass_block-block14) 3)
	(= (z grass_block-block14) 1)
	(= (block-hits grass_block-block14) 0)
	(block-present grass_block-block15)
	(= (x grass_block-block15) -2)
	(= (y grass_block-block15) 3)
	(= (z grass_block-block15) 2)
	(= (block-hits grass_block-block15) 0)
	(block-present grass_block-block16)
	(= (x grass_block-block16) -2)
	(= (y grass_block-block16) 3)
	(= (z grass_block-block16) 3)
	(= (block-hits grass_block-block16) 0)
	(block-present grass_block-block17)
	(= (x grass_block-block17) -2)
	(= (y grass_block-block17) 3)
	(= (z grass_block-block17) 4)
	(= (block-hits grass_block-block17) 0)
	(block-present grass_block-block18)
	(= (x grass_block-block18) -1)
	(= (y grass_block-block18) 3)
	(= (z grass_block-block18) -3)
	(= (block-hits grass_block-block18) 0)
	(block-present grass_block-block19)
	(= (x grass_block-block19) -1)
	(= (y grass_block-block19) 3)
	(= (z grass_block-block19) -2)
	(= (block-hits grass_block-block19) 0)
	(block-present grass_block-block20)
	(= (x grass_block-block20) -1)
	(= (y grass_block-block20) 3)
	(= (z grass_block-block20) -1)
	(= (block-hits grass_block-block20) 0)
	(block-present grass_block-block21)
	(= (x grass_block-block21) -1)
	(= (y grass_block-block21) 3)
	(= (z grass_block-block21) 0)
	(= (block-hits grass_block-block21) 0)
	(block-present grass_block-block22)
	(= (x grass_block-block22) -1)
	(= (y grass_block-block22) 3)
	(= (z grass_block-block22) 0)
	(= (block-hits grass_block-block22) 0)
	(block-present grass_block-block23)
	(= (x grass_block-block23) -1)
	(= (y grass_block-block23) 3)
	(= (z grass_block-block23) 1)
	(= (block-hits grass_block-block23) 0)
	(block-present grass_block-block24)
	(= (x grass_block-block24) -1)
	(= (y grass_block-block24) 3)
	(= (z grass_block-block24) 2)
	(= (block-hits grass_block-block24) 0)
	(block-present grass_block-block25)
	(= (x grass_block-block25) -1)
	(= (y grass_block-block25) 3)
	(= (z grass_block-block25) 3)
	(= (block-hits grass_block-block25) 0)
	(block-present grass_block-block26)
	(= (x grass_block-block26) -1)
	(= (y grass_block-block26) 3)
	(= (z grass_block-block26) 4)
	(= (block-hits grass_block-block26) 0)
	(block-present grass_block-block27)
	(= (x grass_block-block27) 0)
	(= (y grass_block-block27) 3)
	(= (z grass_block-block27) -3)
	(= (block-hits grass_block-block27) 0)
	(block-present grass_block-block28)
	(= (x grass_block-block28) 0)
	(= (y grass_block-block28) 3)
	(= (z grass_block-block28) -2)
	(= (block-hits grass_block-block28) 0)
	(block-present grass_block-block29)
	(= (x grass_block-block29) 0)
	(= (y grass_block-block29) 3)
	(= (z grass_block-block29) -1)
	(= (block-hits grass_block-block29) 0)
	(block-present grass_block-block30)
	(= (x grass_block-block30) 0)
	(= (y grass_block-block30) 3)
	(= (z grass_block-block30) 0)
	(= (block-hits grass_block-block30) 0)
	(block-present grass_block-block31)
	(= (x grass_block-block31) 0)
	(= (y grass_block-block31) 3)
	(= (z grass_block-block31) 0)
	(= (block-hits grass_block-block31) 0)
	(block-present grass_block-block32)
	(= (x grass_block-block32) 0)
	(= (y grass_block-block32) 3)
	(= (z grass_block-block32) 1)
	(= (block-hits grass_block-block32) 0)
	(block-present grass_block-block33)
	(= (x grass_block-block33) 0)
	(= (y grass_block-block33) 3)
	(= (z grass_block-block33) 2)
	(= (block-hits grass_block-block33) 0)
	(block-present grass_block-block34)
	(= (x grass_block-block34) 0)
	(= (y grass_block-block34) 3)
	(= (z grass_block-block34) 3)
	(= (block-hits grass_block-block34) 0)
	(block-present grass_block-block35)
	(= (x grass_block-block35) 0)
	(= (y grass_block-block35) 3)
	(= (z grass_block-block35) 4)
	(= (block-hits grass_block-block35) 0)
	(block-present grass_block-block36)
	(= (x grass_block-block36) 0)
	(= (y grass_block-block36) 3)
	(= (z grass_block-block36) -3)
	(= (block-hits grass_block-block36) 0)
	(block-present grass_block-block37)
	(= (x grass_block-block37) 0)
	(= (y grass_block-block37) 3)
	(= (z grass_block-block37) -2)
	(= (block-hits grass_block-block37) 0)
	(block-present grass_block-block38)
	(= (x grass_block-block38) 0)
	(= (y grass_block-block38) 3)
	(= (z grass_block-block38) -1)
	(= (block-hits grass_block-block38) 0)
	(block-present grass_block-block39)
	(= (x grass_block-block39) 0)
	(= (y grass_block-block39) 3)
	(= (z grass_block-block39) 0)
	(= (block-hits grass_block-block39) 0)
	(block-present grass_block-block40)
	(= (x grass_block-block40) 0)
	(= (y grass_block-block40) 3)
	(= (z grass_block-block40) 0)
	(= (block-hits grass_block-block40) 0)
	(block-present grass_block-block41)
	(= (x grass_block-block41) 0)
	(= (y grass_block-block41) 3)
	(= (z grass_block-block41) 1)
	(= (block-hits grass_block-block41) 0)
	(block-present grass_block-block42)
	(= (x grass_block-block42) 0)
	(= (y grass_block-block42) 3)
	(= (z grass_block-block42) 2)
	(= (block-hits grass_block-block42) 0)
	(block-present grass_block-block43)
	(= (x grass_block-block43) 0)
	(= (y grass_block-block43) 3)
	(= (z grass_block-block43) 3)
	(= (block-hits grass_block-block43) 0)
	(block-present grass_block-block44)
	(= (x grass_block-block44) 0)
	(= (y grass_block-block44) 3)
	(= (z grass_block-block44) 4)
	(= (block-hits grass_block-block44) 0)
	(block-present grass_block-block45)
	(= (x grass_block-block45) 1)
	(= (y grass_block-block45) 3)
	(= (z grass_block-block45) -3)
	(= (block-hits grass_block-block45) 0)
	(block-present grass_block-block46)
	(= (x grass_block-block46) 1)
	(= (y grass_block-block46) 3)
	(= (z grass_block-block46) -2)
	(= (block-hits grass_block-block46) 0)
	(block-present grass_block-block47)
	(= (x grass_block-block47) 1)
	(= (y grass_block-block47) 3)
	(= (z grass_block-block47) -1)
	(= (block-hits grass_block-block47) 0)
	(block-present grass_block-block48)
	(= (x grass_block-block48) 1)
	(= (y grass_block-block48) 3)
	(= (z grass_block-block48) 0)
	(= (block-hits grass_block-block48) 0)
	(block-present grass_block-block49)
	(= (x grass_block-block49) 1)
	(= (y grass_block-block49) 3)
	(= (z grass_block-block49) 0)
	(= (block-hits grass_block-block49) 0)
	(block-present grass_block-block50)
	(= (x grass_block-block50) 1)
	(= (y grass_block-block50) 3)
	(= (z grass_block-block50) 1)
	(= (block-hits grass_block-block50) 0)
	(block-present grass_block-block51)
	(= (x grass_block-block51) 1)
	(= (y grass_block-block51) 3)
	(= (z grass_block-block51) 2)
	(= (block-hits grass_block-block51) 0)
	(block-present grass_block-block52)
	(= (x grass_block-block52) 1)
	(= (y grass_block-block52) 3)
	(= (z grass_block-block52) 3)
	(= (block-hits grass_block-block52) 0)
	(block-present grass_block-block53)
	(= (x grass_block-block53) 1)
	(= (y grass_block-block53) 3)
	(= (z grass_block-block53) 4)
	(= (block-hits grass_block-block53) 0)
	(block-present grass_block-block54)
	(= (x grass_block-block54) 2)
	(= (y grass_block-block54) 3)
	(= (z grass_block-block54) -3)
	(= (block-hits grass_block-block54) 0)
	(block-present grass_block-block55)
	(= (x grass_block-block55) 2)
	(= (y grass_block-block55) 3)
	(= (z grass_block-block55) -2)
	(= (block-hits grass_block-block55) 0)
	(block-present grass_block-block56)
	(= (x grass_block-block56) 2)
	(= (y grass_block-block56) 3)
	(= (z grass_block-block56) -1)
	(= (block-hits grass_block-block56) 0)
	(block-present grass_block-block57)
	(= (x grass_block-block57) 2)
	(= (y grass_block-block57) 3)
	(= (z grass_block-block57) 0)
	(= (block-hits grass_block-block57) 0)
	(block-present grass_block-block58)
	(= (x grass_block-block58) 2)
	(= (y grass_block-block58) 3)
	(= (z grass_block-block58) 0)
	(= (block-hits grass_block-block58) 0)
	(block-present grass_block-block59)
	(= (x grass_block-block59) 2)
	(= (y grass_block-block59) 3)
	(= (z grass_block-block59) 1)
	(= (block-hits grass_block-block59) 0)
	(block-present grass_block-block60)
	(= (x grass_block-block60) 2)
	(= (y grass_block-block60) 3)
	(= (z grass_block-block60) 2)
	(= (block-hits grass_block-block60) 0)
	(block-present grass_block-block61)
	(= (x grass_block-block61) 2)
	(= (y grass_block-block61) 3)
	(= (z grass_block-block61) 3)
	(= (block-hits grass_block-block61) 0)
	(block-present grass_block-block62)
	(= (x grass_block-block62) 2)
	(= (y grass_block-block62) 3)
	(= (z grass_block-block62) 4)
	(= (block-hits grass_block-block62) 0)
	(block-present grass_block-block63)
	(= (x grass_block-block63) 3)
	(= (y grass_block-block63) 3)
	(= (z grass_block-block63) -3)
	(= (block-hits grass_block-block63) 0)
	(block-present grass_block-block64)
	(= (x grass_block-block64) 3)
	(= (y grass_block-block64) 3)
	(= (z grass_block-block64) -2)
	(= (block-hits grass_block-block64) 0)
	(block-present grass_block-block65)
	(= (x grass_block-block65) 3)
	(= (y grass_block-block65) 3)
	(= (z grass_block-block65) -1)
	(= (block-hits grass_block-block65) 0)
	(block-present grass_block-block66)
	(= (x grass_block-block66) 3)
	(= (y grass_block-block66) 3)
	(= (z grass_block-block66) 0)
	(= (block-hits grass_block-block66) 0)
	(block-present grass_block-block67)
	(= (x grass_block-block67) 3)
	(= (y grass_block-block67) 3)
	(= (z grass_block-block67) 0)
	(= (block-hits grass_block-block67) 0)
	(block-present grass_block-block68)
	(= (x grass_block-block68) 3)
	(= (y grass_block-block68) 3)
	(= (z grass_block-block68) 1)
	(= (block-hits grass_block-block68) 0)
	(block-present grass_block-block69)
	(= (x grass_block-block69) 3)
	(= (y grass_block-block69) 3)
	(= (z grass_block-block69) 2)
	(= (block-hits grass_block-block69) 0)
	(block-present grass_block-block70)
	(= (x grass_block-block70) 3)
	(= (y grass_block-block70) 3)
	(= (z grass_block-block70) 3)
	(= (block-hits grass_block-block70) 0)
	(block-present grass_block-block71)
	(= (x grass_block-block71) 3)
	(= (y grass_block-block71) 3)
	(= (z grass_block-block71) 4)
	(= (block-hits grass_block-block71) 0)
	(block-present grass_block-block72)
	(= (x grass_block-block72) 4)
	(= (y grass_block-block72) 3)
	(= (z grass_block-block72) -3)
	(= (block-hits grass_block-block72) 0)
	(block-present grass_block-block73)
	(= (x grass_block-block73) 4)
	(= (y grass_block-block73) 3)
	(= (z grass_block-block73) -2)
	(= (block-hits grass_block-block73) 0)
	(block-present grass_block-block74)
	(= (x grass_block-block74) 4)
	(= (y grass_block-block74) 3)
	(= (z grass_block-block74) -1)
	(= (block-hits grass_block-block74) 0)
	(block-present grass_block-block75)
	(= (x grass_block-block75) 4)
	(= (y grass_block-block75) 3)
	(= (z grass_block-block75) 0)
	(= (block-hits grass_block-block75) 0)
	(block-present grass_block-block76)
	(= (x grass_block-block76) 4)
	(= (y grass_block-block76) 3)
	(= (z grass_block-block76) 0)
	(= (block-hits grass_block-block76) 0)
	(block-present grass_block-block77)
	(= (x grass_block-block77) 4)
	(= (y grass_block-block77) 3)
	(= (z grass_block-block77) 1)
	(= (block-hits grass_block-block77) 0)
	(block-present grass_block-block78)
	(= (x grass_block-block78) 4)
	(= (y grass_block-block78) 3)
	(= (z grass_block-block78) 2)
	(= (block-hits grass_block-block78) 0)
	(block-present grass_block-block79)
	(= (x grass_block-block79) 4)
	(= (y grass_block-block79) 3)
	(= (z grass_block-block79) 3)
	(= (block-hits grass_block-block79) 0)
	(block-present grass_block-block80)
	(= (x grass_block-block80) 4)
	(= (y grass_block-block80) 3)
	(= (z grass_block-block80) 4)
	(= (block-hits grass_block-block80) 0)
	(block-present obsidian-block0)
	(= (x obsidian-block0) 4)
	(= (y obsidian-block0) 4)
	(= (z obsidian-block0) 0)
	(= (block-hits obsidian-block0) 0)
	(block-present log-block0)
	(= (x log-block0) 4)
	(= (y log-block0) 5)
	(= (z log-block0) -3)
	(= (block-hits log-block0) 0)
	(item-present diamond0)
	(= (x diamond0) 1)
	(= (y diamond0) 4)
	(= (z diamond0) 5)
	(item-present oak-log0)
	(= (x oak-log0) 0)
	(= (y oak-log0) 4)
	(= (z oak-log0) 5)
	(not (item-present log0))
	(= (x log0) 0)
	(= (y log0) 4)
	(= (z log0) 0)
	(not (item-present obsidian0))
	(= (x obsidian0) 0)
	(= (y obsidian0) 4)
	(= (z obsidian0) 0)
)
(:goal
	(and (goal-achieved steve))
		
)
)