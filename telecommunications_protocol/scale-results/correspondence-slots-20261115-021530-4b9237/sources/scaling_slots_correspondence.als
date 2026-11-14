module scaling_slots_correspondence

open telecommunications as original
open telecommunications_slots as slots
open util/sequniv as seqLib

// Small-scope comparison of the sequence-route model and the arity-2,
// arithmetic-free slot encoding. The slot side has exactly two singleton
// snapshots, Before and After, and four data slots per history.
// Sequence index i of the original corresponds to slot Si.
// No fact assumes either representation's sectional invariant.
// These checks compare REPRESENTED state/transition pairs at small bounds.
// They are not an unbounded equivalence theorem, and they inherit the
// ordered-pool insertion-enabledness qualification of scaling_design.md.
one sig Bridge {
  points: original/SPC one -> one slots/SPC,
  messages: original/Message one -> one slots/Message
}

fun indexSlot: Int -> slots/Slot {
  0 -> slots/S0 + 1 -> slots/S1 + 2 -> slots/S2 + 3 -> slots/S3
}

// Translate an original history (seq/Int -> Message) to a slot history.
fun asSlots[h: Int -> original/Message]: slots/Slot -> slots/Message {
  (~indexSlot).h.(Bridge.messages)
}

pred corresponding[a: original/State, b: slots/State] {
  // A sequence route must be well-formed to interpret its ordering. This
  // constrains representation shape only, not history accounting or validity.
  seqLib/isSeq[a.route]
  some a.route
  not seqLib/hasDups[a.route]
  b.route = seqLib/elems[a.route].(Bridge.points)
  seqLib/first[a.route].(Bridge.points) = slots/firstPoint[b]
  all i: seqLib/inds[a.route] - seqLib/lastIdx[a.route] |
    a.route[add[i, 1]].(Bridge.points) =
      slots/nextPoint[b, a.route[i].(Bridge.points)]
  all p: original/SPC | {
    // Every original history entry must have a slot (indices 0..3).
    (a.rec[p] + a.ins[p] + a.sent[p]).original/Message in indexSlot.slots/Slot
    slots/received[b, p.(Bridge.points)] = asSlots[a.rec[p]]
    slots/pending[b, p.(Bridge.points)] = asSlots[a.ins[p]]
    slots/departed[b, p.(Bridge.points)] = asSlots[a.sent[p]]
  }
}

assert SectionInvariantsCorrespond {
  all a: original/State, b: slots/State |
    corresponding[a, b] implies
      (original/sectionInvariant[a] iff slots/sectionInvariant[b])
}

assert InitialStatesCorrespond {
  all a: original/State, b: slots/State |
    corresponding[a, b] implies
      (original/initial[a] iff slots/initial[b])
}

assert RetrieveObservationsCorrespond {
  all a: original/State, b: slots/State |
    (corresponding[a, b] and original/sectionInvariant[a]) implies {
      asSlots[original/input[a]] = slots/input[b]
      asSlots[original/output[a]] = slots/output[b]
      asSlots[original/inFlight[a]] = slots/inFlight[b]
    }
}

assert TransmitEffectsCorrespond {
  all a, b: original/State, c, d: slots/State, m: original/Message |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies
      (original/transmit[a, b, m] iff
       slots/transmit[c, d, m.(Bridge.messages)])
}

assert ReceiveEffectsCorrespond {
  all a, b: original/State, c, d: slots/State |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies {
      original/receive[a, b] iff slots/receive[c, d]
      original/receivePoll[a, b] iff slots/receivePoll[c, d]
    }
}

assert DaemonEffectsCorrespond {
  all a, b: original/State, c, d: slots/State, p: original/SPC |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies {
      original/daemon[a, b, p] iff
        slots/daemon[c, d, p.(Bridge.points)]
      original/daemonOrIdle[a, b] iff slots/daemonOrIdle[c, d]
    }
}

assert InsertionEffectsCorrespond {
  all a, b: original/State, c, d: slots/State, p, fresh: original/SPC |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies
      (original/insertSection[a, b, p, fresh] iff
       slots/insertSection[c, d, p.(Bridge.points), fresh.(Bridge.points)])
}

// The external specification is checked separately because it is where the
// slot encoding replaces # and integer offsets by slot shifts.
// Histories are drawn from arbitrary (not necessarily valid) state fields.
assert ExternalPredicatesCorrespond {
  all a, b: original/State, h1, h2: original/SPC |
    let x = a.rec[h1], y = b.sent[h2] |
      (seqLib/isSeq[x] and seqLib/isSeq[y] and
       (x + y).original/Message in indexSlot.slots/Slot) implies {
        original/suffix[x, y] iff slots/suffix[asSlots[x], asSlots[y]]
        (#y = add[#x, 1]) iff
          (slots/marker[asSlots[x]].(slots/shift1) = slots/marker[asSlots[y]])
      }
}

// Positive cases make the representation relation and transition comparisons
// demonstrably satisfiable. Neither witness assumes a post-state invariant.
pred ShowCorrespondingTransmit {
  some disj a, b: original/State, disj c, d: slots/State,
       m: original/Message |
    corresponding[a, c] and corresponding[b, d] and
    original/initial[a] and slots/initial[c] and
    original/transmit[a, b, m] and
    slots/transmit[c, d, m.(Bridge.messages)]
}

pred ShowCorrespondingInsertion {
  some disj a, b: original/State, disj c, d: slots/State,
       p, fresh: original/SPC |
    corresponding[a, c] and corresponding[b, d] and
    original/sectionInvariant[a] and slots/sectionInvariant[c] and
    some original/inFlight[a] and some a.sent[p] and
    original/insertSection[a, b, p, fresh] and
    slots/insertSection[c, d, p.(Bridge.points), fresh.(Bridge.points)]
}

pred ShowCorrespondingReceive {
  some disj a, b: original/State, disj c, d: slots/State |
    corresponding[a, c] and corresponding[b, d] and
    original/sectionInvariant[a] and slots/sectionInvariant[c] and
    original/receive[a, b] and slots/receive[c, d]
}

pred ShowCorrespondingDaemon {
  some disj a, b: original/State, disj c, d: slots/State,
       p: original/SPC |
    corresponding[a, c] and corresponding[b, d] and
    original/sectionInvariant[a] and slots/sectionInvariant[c] and
    original/daemon[a, b, p] and
    slots/daemon[c, d, p.(Bridge.points)]
}

// Three points in each pool, at most three message values, histories bounded
// by four entries on both sides (4 seq; four data slots), and 6-bit integers
// covering the original model's raw 3 * 4 offset sums.
check SectionInvariantsCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
check InitialStatesCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
check RetrieveObservationsCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
check TransmitEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
check ReceiveEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
check DaemonEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
check InsertionEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
check ExternalPredicatesCorrespond for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 0
run ShowCorrespondingTransmit for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 1
run ShowCorrespondingInsertion for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 1
run ShowCorrespondingReceive for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 1
run ShowCorrespondingDaemon for 3 but exactly 2 original/State, exactly 2 slots/State, 6 Int, 4 seq expect 1
