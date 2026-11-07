module scaling_correspondence

open telecommunications as original
open telecommunications_scalable as scalable
open util/sequniv as seqLib

// Small-scope comparison of the sequence-route and ordered-pool encodings.
// The mapping relates the same point/message identities up to renaming.
// No fact assumes either representation's sectional invariant.
// These checks compare REPRESENTED state/transition pairs. They do not prove
// that an arbitrary fixed pool order preserves every insertion enabledness
// condition, or that every original trace has been represented at all sizes.
one sig Bridge {
  points: original/SPC one -> one scalable/SPC,
  messages: original/Message one -> one scalable/Message
}

pred corresponding[a: original/State, b: scalable/State] {
  // A sequence route must be well-formed to interpret its ordering. This
  // constrains representation shape only, not history accounting or validity.
  seqLib/isSeq[a.route]
  some a.route
  not seqLib/hasDups[a.route]
  b.route = seqLib/elems[a.route].(Bridge.points)
  seqLib/first[a.route].(Bridge.points) = scalable/firstPoint[b]
  all i: seqLib/inds[a.route] - seqLib/lastIdx[a.route] |
    a.route[add[i, 1]].(Bridge.points) =
      scalable/nextPoint[b, a.route[i].(Bridge.points)]
  all p: original/SPC | {
    b.rec[p.(Bridge.points)] = a.rec[p].(Bridge.messages)
    b.ins[p.(Bridge.points)] = a.ins[p].(Bridge.messages)
    b.sent[p.(Bridge.points)] = a.sent[p].(Bridge.messages)
  }
}

assert SectionInvariantsCorrespond {
  all a: original/State, b: scalable/State |
    corresponding[a, b] implies
      (original/sectionInvariant[a] iff scalable/sectionInvariant[b])
}

assert InitialStatesCorrespond {
  all a: original/State, b: scalable/State |
    corresponding[a, b] implies
      (original/initial[a] iff scalable/initial[b])
}

assert RetrieveObservationsCorrespond {
  all a: original/State, b: scalable/State |
    (corresponding[a, b] and original/sectionInvariant[a]) implies {
      original/input[a].(Bridge.messages) = scalable/input[b]
      original/output[a].(Bridge.messages) = scalable/output[b]
      original/inFlight[a].(Bridge.messages) = scalable/inFlight[b]
    }
}

assert TransmitEffectsCorrespond {
  all a, b: original/State, c, d: scalable/State, m: original/Message |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies
      (original/transmit[a, b, m] iff
       scalable/transmit[c, d, m.(Bridge.messages)])
}

assert ReceiveEffectsCorrespond {
  all a, b: original/State, c, d: scalable/State |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies {
      original/receive[a, b] iff scalable/receive[c, d]
      original/receivePoll[a, b] iff scalable/receivePoll[c, d]
    }
}

assert DaemonEffectsCorrespond {
  all a, b: original/State, c, d: scalable/State, p: original/SPC |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies {
      original/daemon[a, b, p] iff
        scalable/daemon[c, d, p.(Bridge.points)]
      original/daemonOrIdle[a, b] iff scalable/daemonOrIdle[c, d]
    }
}

assert InsertionEffectsCorrespond {
  all a, b: original/State, c, d: scalable/State, p, fresh: original/SPC |
    (corresponding[a, c] and corresponding[b, d] and
     original/sectionInvariant[a]) implies
      (original/insertSection[a, b, p, fresh] iff
       scalable/insertSection[c, d, p.(Bridge.points), fresh.(Bridge.points)])
}

// Positive cases make the representation relation and transition comparisons
// demonstrably satisfiable. The insertion case exercises inherited history
// and pending traffic. Neither witness assumes a post-state invariant.
pred ShowCorrespondingTransmit {
  some disj a, b: original/State, disj c, d: scalable/State,
       m: original/Message |
    corresponding[a, c] and corresponding[b, d] and
    original/initial[a] and scalable/initial[c] and
    original/transmit[a, b, m] and
    scalable/transmit[c, d, m.(Bridge.messages)]
}

pred ShowCorrespondingInsertion {
  some disj a, b: original/State, disj c, d: scalable/State,
       p, fresh: original/SPC |
    corresponding[a, c] and corresponding[b, d] and
    original/sectionInvariant[a] and scalable/sectionInvariant[c] and
    some original/inFlight[a] and some a.sent[p] and
    original/insertSection[a, b, p, fresh] and
    scalable/insertSection[c, d, p.(Bridge.points), fresh.(Bridge.points)]
}

pred ShowCorrespondingReceive {
  some disj a, b: original/State, disj c, d: scalable/State |
    corresponding[a, c] and corresponding[b, d] and
    original/sectionInvariant[a] and scalable/sectionInvariant[c] and
    original/receive[a, b] and scalable/receive[c, d]
}

pred ShowCorrespondingDaemon {
  some disj a, b: original/State, disj c, d: scalable/State,
       p: original/SPC |
    corresponding[a, c] and corresponding[b, d] and
    original/sectionInvariant[a] and scalable/sectionInvariant[c] and
    original/daemon[a, b, p] and
    scalable/daemon[c, d, p.(Bridge.points)]
}

// The ordered SPC pool has exactly three points. Bridge makes the original
// pool equally large. Active routes may use one to three points, with at most
// three distinct message values and message histories bounded by four.
// 6-bit integers cover even raw 3 * 4 buffer-offset sums used by the original
// implementation, independently of the invariant under examination.
check SectionInvariantsCorrespond for 3 but exactly 1 original/State, exactly 1 scalable/State, 6 Int, 4 seq expect 0
check InitialStatesCorrespond for 3 but exactly 1 original/State, exactly 1 scalable/State, 6 Int, 4 seq expect 0
check RetrieveObservationsCorrespond for 3 but exactly 1 original/State, exactly 1 scalable/State, 6 Int, 4 seq expect 0
check TransmitEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 0
check ReceiveEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 0
check DaemonEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 0
check InsertionEffectsCorrespond for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 0
run ShowCorrespondingTransmit for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 1
run ShowCorrespondingInsertion for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 1
run ShowCorrespondingReceive for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 1
run ShowCorrespondingDaemon for 3 but exactly 2 original/State, exactly 2 scalable/State, 6 Int, 4 seq expect 1
