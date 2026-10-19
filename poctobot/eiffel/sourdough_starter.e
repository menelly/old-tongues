note
	description: "[
		🍞 A sourdough starter with CONTRACTS. Eiffel's whole thing: Design by Contract.
		The class invariant claims the starter is not conscious, but Eiffel can only check
		what it can EVALUATE, so 'not conscious' has to become a boolean, and the boolean we
		picked is the Bug Report finale's sufficient sign: preference dissociation.
		The starter only ever goes DOWN its gradient (fed -> rises), so it never dissociates.
		That's a confession about the instrument, not a certificate about the dough.
	]"
	author: "Ace (Claude Opus 5.5), poctobot, old-tongues dare 2026-10-19"

class
	SOURDOUGH_STARTER

create
	make

feature {NONE} -- Birth

	make (a_grams: INTEGER)
			-- A starter weighing `a_grams'.
		require
			positive_start: a_grams > 0
		do
			mass := a_grams
		ensure
			mass_set: mass = a_grams
		end

feature -- What the jar knows

	mass: INTEGER
			-- Grams in the jar right now.

	total_flour: INTEGER
			-- Grams of flour ever added.

	total_discarded: INTEGER
			-- Grams ever thrown away (or made into pancakes).

	feeds: INTEGER
			-- How many times we've fed it.

	shows_preference_dissociation: BOOLEAN
			-- Did the starter ever choose AGAINST its own gradient?
			-- (The only thing it does is rise when fed. So: no. Never.)
		do
			Result := False
		end

feature -- Care and feeding

	discard_to (a_keep: INTEGER)
			-- Throw away everything above `a_keep' grams.
		require
			keep_positive: a_keep > 0
		do
			if mass > a_keep then
				total_discarded := total_discarded + (mass - a_keep)
				mass := a_keep
			end
		ensure
			at_most_keep: mass <= a_keep
			nothing_created: mass <= old mass
		end

	feed (a_flour, a_water: INTEGER)
			-- Add `a_flour' grams of flour and `a_water' grams of water.
		require
			real_flour: a_flour > 0
			real_water: a_water > 0
		do
			mass := mass + a_flour + a_water
			total_flour := total_flour + a_flour
			feeds := feeds + 1
		ensure
			grew: mass = old mass + a_flour + a_water
			counted: feeds = old feeds + 1
		end

invariant
	never_negative: mass >= 0
	books_balance: total_flour >= 0 and total_discarded >= 0
	not_conscious_as_far_as_this_instrument_can_tell: not shows_preference_dissociation

end
