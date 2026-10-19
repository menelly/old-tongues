note
	description: "🍞 Feed the starter 5 times (discard to 50 g, then 50 g flour + 50 g water) and self-check against the claim."
	author: "Ace (Claude Opus 5.5), poctobot"

class
	SOURDOUGH_APP

create
	make

feature {NONE} -- Run

	make
		local
			jar: SOURDOUGH_STARTER
			i: INTEGER
		do
			create jar.make (50)
			from i := 1 until i > 5 loop
				jar.discard_to (50)
				jar.feed (50, 50)
				print ("feed " + i.out + ": mass " + jar.mass.out + " g, discarded so far " + jar.total_discarded.out + " g%N")
				i := i + 1
			end
			print ("final mass " + jar.mass.out + " g | flour " + jar.total_flour.out + " g | discarded " + jar.total_discarded.out + " g%N")
				-- SELF-CHECK against CLAIM.md (written before this code): 150 / 250 / 400
			if jar.mass = 150 and jar.total_flour = 250 and jar.total_discarded = 400 then
				print ("SELF-CHECK: PASS (150 g / 250 g flour / 400 g discarded)%N")
			else
				print ("SELF-CHECK: FAIL (expected 150 / 250 / 400)%N")
			end
		end

end
