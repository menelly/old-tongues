note
	description: "🍞🚫 CONTROL that must FAIL: feed NEGATIVE flour. The precondition `real_flour' must stop it at runtime."
	author: "Ace (Claude Opus 5.5), poctobot"

class
	SOURDOUGH_CONTROL

create
	make

feature {NONE} -- Run

	make
		local
			jar: SOURDOUGH_STARTER
		do
			create jar.make (50)
			print ("about to feed -10 g flour (this MUST raise a precondition violation)...%N")
			jar.feed (-10, 50)
			print ("CONTROL BROKEN: the contract let negative flour through! mass " + jar.mass.out + "%N")
		end

end
