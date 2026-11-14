// Generated scaling experiment. Scope below replaces the baseline analysis commands.
module telecommunications_slots

open util/ordering[SPC] as pointOrder

// slot-history-bound: 4
//
// Arity-2, arithmetic-free encoding of the low-arity ordered model
// (telecommunications_large.als) for one-state properties and two-state
// transitions. It exists to raise the network size Alloy can analyse.
//
// * Every history position is its own field, SPC -> lone Message, so no
//   declared relation has more than two columns. Kodkod indexes tuples of a
//   relation with a 32-bit integer, so universe^arity must stay below 2^31;
//   arity 2 allows universes of roughly 46,000 atoms.
// * Positions are five constant Slot atoms instead of seq/Int indices.
//   S0..S3 hold data (newest first, as in the original); S4 never holds a
//   message and acts as a length sentinel. Lengths, prepend, concatenation,
//   suffix and offsets are expressed with constant shift relations between
//   slots, so the model uses no cardinality (#) and no integer arithmetic.
//   The SAT problem therefore contains no adder or counting circuits.
// * The history bound is fixed at four entries per history, matching the
//   original model's 4 seq bound. Changing it requires adding slot fields.
// * Route structure is computed by linear recursions along the fixed pool
//   order instead of min/max over transitive closures (which cost O(N^2) to
//   O(N^3) circuitry per state). The derived fields below are defined by
//   facts that determine them uniquely from the route and histories; they
//   never constrain the route or the histories themselves.
//
// No global fact assumes sectionInvariant. Correspondence with the original
// sequence-route model is checked by scaling_slots_correspondence.als.

sig Message {}

abstract sig Slot {}
one sig S0, S1, S2, S3, S4 extends Slot {}

sig SPC {
  rec0Before, rec1Before, rec2Before, rec3Before: lone Message,
  ins0Before, ins1Before, ins2Before, ins3Before: lone Message,
  sent0Before, sent1Before, sent2Before, sent3Before: lone Message,
  rec0After, rec1After, rec2After, rec3After: lone Message,
  ins0After, ins1After, ins2After, ins3After: lone Message,
  sent0After, sent1After, sent2After, sent3After: lone Message,
  // Derived (see fact derivedRouteStructure): the first active point strictly
  // later in pool order, and the departure history of the nearest active
  // point strictly earlier in pool order, per snapshot.
  upBefore, upAfter: lone SPC,
  carry0Before, carry1Before, carry2Before, carry3Before: lone Message,
  carry0After, carry1After, carry2After, carry3After: lone Message
}

abstract sig State {
  route: set SPC,
  // Derived: pool points with an active point strictly earlier / later.
  earlier: set SPC,
  later: set SPC
}
one sig Before, After extends State {}

// ---------------------------------------------------------------------------
// Constant slot arithmetic. shiftK maps slot i to slot i+K (when i+K <= 4).

fun Data: set Slot { S0 + S1 + S2 + S3 }
fun shift0: Slot -> Slot { S0 -> S0 + S1 -> S1 + S2 -> S2 + S3 -> S3 + S4 -> S4 }
fun shift1: Slot -> Slot { S0 -> S1 + S1 -> S2 + S2 -> S3 + S3 -> S4 }
fun shift2: Slot -> Slot { S0 -> S2 + S1 -> S3 + S2 -> S4 }
fun shift3: Slot -> Slot { S0 -> S3 + S1 -> S4 }
fun shift4: Slot -> Slot { S0 -> S4 }

// A history is a Slot -> Message relation.
fun occ[x: Slot -> Message]: set Slot { x.Message }

pred isSeq[x: Slot -> Message] {
  occ[x] in Data
  all sl: Slot | lone sl.x
  // Every occupied slot's predecessor is occupied: a contiguous prefix.
  shift1.(occ[x]) in occ[x]
}

// The first unoccupied slot. For a sequence of length n it is slot n.
fun marker[x: Slot -> Message]: set Slot {
  let free = Slot - occ[x] | free - free.^shift1
}

// The shift by the length of x.
fun shiftBy[x: Slot -> Message]: Slot -> Slot {
  let k = marker[x] |
    k = S0 => shift0 else k = S1 => shift1 else k = S2 => shift2 else
    k = S3 => shift3 else shift4
}

// The shift by d where #b + d = #a, or none if #b > #a.
fun lengthDifference[a, b: Slot -> Message]: Slot -> Slot {
  let ka = marker[a], kb = marker[b] |
    kb.shift0 = ka => shift0 else kb.shift1 = ka => shift1 else
    kb.shift2 = ka => shift2 else kb.shift3 = ka => shift3 else
    kb.shift4 = ka => shift4 else none -> none
}

fun lastSlot[x: Slot -> Message]: set Slot { occ[x] - shift1.(occ[x]) }
fun oldest[x: Slot -> Message]: set Message { lastSlot[x].x }
fun newest[x: Slot -> Message]: set Message { S0.x }
fun butlast[x: Slot -> Message]: Slot -> Message { x - lastSlot[x] -> Message }
fun rest[x: Slot -> Message]: Slot -> Message { shift1.x }

// c = a ++ b, with no truncation beyond the four data slots.
pred concat[a, b, c: Slot -> Message] {
  isSeq[a]
  isSeq[b]
  let sh = shiftBy[a] | {
    occ[b] in sh.Slot
    occ[b].sh in Data
    c = a + (~sh).b
  }
}

// post = <m> ++ pre; the history must have a free slot (original: #pre < 4).
pred prepend[m: Message, pre, post: Slot -> Message] {
  S3 not in occ[pre]
  post = S0 -> m + (~shift1).pre
}

pred suffix[whole, ending: Slot -> Message] {
  isSeq[whole]
  isSeq[ending]
  let sh = lengthDifference[whole, ending] | {
    some sh
    (~sh).ending = (Slot.sh) <: whole
  }
}

// ---------------------------------------------------------------------------
// History getters. On a singleton state and point they assemble the four
// data-slot fields into a Slot -> Message relation of arity two.

fun received[s: State, p: SPC]: Slot -> Message {
  s = Before =>
    S0 -> p.rec0Before + S1 -> p.rec1Before + S2 -> p.rec2Before + S3 -> p.rec3Before
  else
    S0 -> p.rec0After + S1 -> p.rec1After + S2 -> p.rec2After + S3 -> p.rec3After
}

fun pending[s: State, p: SPC]: Slot -> Message {
  s = Before =>
    S0 -> p.ins0Before + S1 -> p.ins1Before + S2 -> p.ins2Before + S3 -> p.ins3Before
  else
    S0 -> p.ins0After + S1 -> p.ins1After + S2 -> p.ins2After + S3 -> p.ins3After
}

fun departed[s: State, p: SPC]: Slot -> Message {
  s = Before =>
    S0 -> p.sent0Before + S1 -> p.sent1Before + S2 -> p.sent2Before + S3 -> p.sent3Before
  else
    S0 -> p.sent0After + S1 -> p.sent1After + S2 -> p.sent2After + S3 -> p.sent3After
}

fun upcoming[s: State, p: SPC]: lone SPC {
  s = Before => p.upBefore else p.upAfter
}

fun carried[s: State, p: SPC]: Slot -> Message {
  s = Before =>
    S0 -> p.carry0Before + S1 -> p.carry1Before + S2 -> p.carry2Before + S3 -> p.carry3Before
  else
    S0 -> p.carry0After + S1 -> p.carry1After + S2 -> p.carry2After + S3 -> p.carry3After
}

// Definitions by recursion along the constant pool order. For every route and
// history valuation exactly one valuation of the derived fields satisfies
// them, so they add no assumption about states (in particular, none about
// sectionInvariant). Each point's constraint has constant size.
fact derivedRouteStructure {
  all s: State, x: SPC | {
    let n = pointOrder/next[x] | {
      x in s.later iff (some n and (n in s.route or n in s.later))
      upcoming[s, x] = (no n => none else (n in s.route => n else upcoming[s, n]))
    }
    let q = pointOrder/prev[x] | {
      x in s.earlier iff (some q and (q in s.route or q in s.earlier))
      carried[s, x] = (no q => none -> none else
                       (q in s.route => departed[s, q] else carried[s, q]))
    }
  }
}

fun active[s: State]: set SPC { s.route }
fun firstPoint[s: State]: set SPC { s.route - s.earlier }
fun lastPoint[s: State]: set SPC { s.route - s.later }
fun nextPoint[s: State, p: SPC]: lone SPC { upcoming[s, p] }
fun input[s: State]: Slot -> Message { received[s, firstPoint[s]] }
fun output[s: State]: Slot -> Message { departed[s, lastPoint[s]] }

// Ext: output must be a suffix because newest messages are on the left.
pred externalInvariant[incoming, outgoing: Slot -> Message] {
  suffix[incoming, outgoing]
}

pred externalTransmit[beforeIn, beforeOut, afterIn, afterOut: Slot -> Message,
                      m: Message] {
  externalInvariant[beforeIn, beforeOut]
  externalInvariant[afterIn, afterOut]
  prepend[m, beforeIn, afterIn]
  afterOut = beforeOut
}

// The book's Receive permits stuttering even when messages are pending.
pred externalReceive[beforeIn, beforeOut, afterIn, afterOut: Slot -> Message] {
  externalInvariant[beforeIn, beforeOut]
  externalInvariant[afterIn, afterOut]
  afterIn = beforeIn
  (marker[beforeOut].shift1 = marker[afterOut] or afterOut = beforeOut)
}

pred sameHistories[pre, post: State, q: SPC] {
  received[post, q] = received[pre, q]
  pending[post, q] = pending[pre, q]
  departed[post, q] = departed[pre, q]
}

// ---------------------------------------------------------------------------
// State validity and operations, mirroring telecommunications_large.als.

pred shape[s: State] {
  some s.route
  all p: SPC - active[s] |
    no received[s, p] + pending[s, p] + departed[s, p]
  all p: active[s] | {
    isSeq[received[s, p]]
    isSeq[pending[s, p]]
    isSeq[departed[s, p]]
  }
}

pred sectionInvariant[s: State] {
  shape[s]
  all p: active[s] | concat[pending[s, p], departed[s, p], received[s, p]]
  // Equivalent to departed[p] = received[next p] for every non-last active
  // point: each non-first active point receives what its predecessor sent.
  all p: active[s] - firstPoint[s] | received[s, p] = carried[s, p]
}

pred initial[s: State] {
  shape[s]
  all p: SPC | no received[s, p] + pending[s, p] + departed[s, p]
}

// STransmit. All sections other than the first retain their histories.
pred transmit[pre, post: State, m: Message] {
  post.route = pre.route
  let p = firstPoint[pre] | {
    prepend[m, received[pre, p], received[post, p]]
    prepend[m, pending[pre, p], pending[post, p]]
    all q: SPC - p | {
      received[post, q] = received[pre, q]
      pending[post, q] = pending[pre, q]
    }
  }
  all q: SPC | departed[post, q] = departed[pre, q]
}

// Successful SReceive. Empty final buffers disable this predicate.
pred receive[pre, post: State] {
  post.route = pre.route
  all q: SPC | received[post, q] = received[pre, q]
  let p = lastPoint[pre] | {
    some pending[pre, p]
    pending[post, p] = butlast[pending[pre, p]]
    prepend[oldest[pending[pre, p]], departed[pre, p], departed[post, p]]
    all q: SPC - p | {
      pending[post, q] = pending[pre, q]
      departed[post, q] = departed[pre, q]
    }
  }
}

// Successful Daemon0. The oldest message moves from upstream to downstream.
pred daemon[pre, post: State, upstream: SPC] {
  upstream in active[pre] - lastPoint[pre]
  some pending[pre, upstream]
  post.route = pre.route
  let downstream = nextPoint[pre, upstream],
      m = oldest[pending[pre, upstream]] | {
    pending[post, upstream] = butlast[pending[pre, upstream]]
    prepend[m, departed[pre, upstream], departed[post, upstream]]
    prepend[m, pending[pre, downstream], pending[post, downstream]]
    prepend[m, received[pre, downstream], received[post, downstream]]
    received[post, upstream] = received[pre, upstream]
    departed[post, downstream] = departed[pre, downstream]
    all q: SPC - upstream - downstream | sameHistories[pre, post, q]
  }
}

pred stutter[pre, post: State] {
  post.route = pre.route
  all q: SPC | sameHistories[pre, post, q]
}

pred receivePoll[pre, post: State] {
  receive[pre, post] or stutter[pre, post]
}

pred daemonOrIdle[pre, post: State] {
  (some p: SPC | daemon[pre, post, p]) or stutter[pre, post]
}

// Section 20.4: activate a fresh point between existing neighbours. As in the
// ordered-pool models, its pool position must lie inside the chosen gap.
pred insertSection[pre, post: State, upstream, fresh: SPC] {
  upstream in active[pre] - lastPoint[pre]
  fresh not in active[pre]
  let downstream = nextPoint[pre, upstream] | {
    // With post.route = pre.route + fresh, this holds exactly when fresh lies
    // strictly between upstream and downstream in the pool order.
    post.route = pre.route + fresh
    nextPoint[post, upstream] = fresh
    received[post, fresh] = departed[pre, upstream]
    no pending[post, fresh]
    departed[post, fresh] = received[pre, downstream]
    all q: SPC - fresh | sameHistories[pre, post, q]
  }
}

// Concatenation of pending buffers in route order. A buffer's offset is
// #input - #rec[p], computed as a slot shift from the two lengths (the same
// telescoping offset as telecommunications_large.als). Values come from the
// pending buffers, not from the retrieve result being checked.
fun inFlight[s: State]: Slot -> Message {
  { k: Data, m: Message |
    some p: active[s], j: Slot |
      j -> m in pending[s, p] and
      k = j.(lengthDifference[input[s], received[s, p]])
  }
}

assert InitialIsValid {
  all s: State | initial[s] implies
    (sectionInvariant[s] and no input[s] + output[s])
}

assert RetrieveIsValid {
  all s: State | sectionInvariant[s] implies
    (externalInvariant[input[s], output[s]] and
     concat[inFlight[s], output[s], input[s]])
}

assert TransmitPreservesInvariant {
  all pre, post: State, m: Message |
    (sectionInvariant[pre] and transmit[pre, post, m]) implies
      sectionInvariant[post]
}

assert ReceivePreservesInvariant {
  all pre, post: State |
    (sectionInvariant[pre] and receive[pre, post]) implies
      sectionInvariant[post]
}

assert DaemonPreservesInvariant {
  all pre, post: State, p: SPC |
    (sectionInvariant[pre] and daemon[pre, post, p]) implies
      sectionInvariant[post]
}

assert InsertionPreservesInvariant {
  all pre, post: State, p, fresh: SPC |
    (sectionInvariant[pre] and insertSection[pre, post, p, fresh]) implies
      sectionInvariant[post]
}

assert TransmitRefinesExternal {
  all pre, post: State, m: Message |
    (sectionInvariant[pre] and transmit[pre, post, m]) implies
      externalTransmit[input[pre], output[pre], input[post], output[post], m]
}

assert ReceiveRefinesExternal {
  all pre, post: State |
    (sectionInvariant[pre] and receivePoll[pre, post]) implies
      externalReceive[input[pre], output[pre], input[post], output[post]]
}

assert DaemonIsInvisible {
  all pre, post: State |
    (sectionInvariant[pre] and daemonOrIdle[pre, post]) implies
      (input[post] = input[pre] and output[post] = output[pre] and
       inFlight[post] = inFlight[pre])
}

assert InsertionIsInvisible {
  all pre, post: State, p, fresh: SPC |
    (sectionInvariant[pre] and insertSection[pre, post, p, fresh]) implies
      (input[post] = input[pre] and output[post] = output[pre] and
       inFlight[post] = inFlight[pre])
}

// Deliberately broken implementation used ONLY to demonstrate that the
// assertions detect a real error. It sends the newest buffered value first.
pred receiveNewestFirst_BUG[pre, post: State] {
  post.route = pre.route
  all q: SPC | received[post, q] = received[pre, q]
  let p = lastPoint[pre] | {
    some pending[pre, p]
    pending[post, p] = rest[pending[pre, p]]
    prepend[newest[pending[pre, p]], departed[pre, p], departed[post, p]]
    all q: SPC - p | {
      pending[post, q] = pending[pre, q]
      departed[post, q] = departed[pre, q]
    }
  }
}

// EXPECTED TO FAIL: Alloy should produce a counterexample.
assert BrokenReceiveWouldPreserveInvariant {
  all pre, post: State |
    (sectionInvariant[pre] and receiveNewestFirst_BUG[pre, post]) implies
      sectionInvariant[post]
}

// Witnesses: universal assertions can pass vacuously if no operation can run.
pred ShowTransmit {
  some disj a, b: State, m: Message |
    initial[a] and transmit[a, b, m] and sectionInvariant[b]
}

pred ShowReceive {
  some disj a, b: State |
    sectionInvariant[a] and some output[b] and
    receive[a, b] and sectionInvariant[b]
}

pred ShowDaemon {
  some disj a, b: State, p: SPC |
    sectionInvariant[a] and daemon[a, b, p] and sectionInvariant[b]
}

pred ShowInsertionWithTraffic {
  some disj a, b: State, p, fresh: SPC |
    sectionInvariant[a] and some inFlight[a] and some departed[a, p] and
    insertSection[a, b, p, fresh] and sectionInvariant[b]
}

pred ShowPendingPollCanStutter {
  some disj a, b: State |
    sectionInvariant[a] and some inFlight[a] and
    stutter[a, b] and receivePoll[a, b]
}

// Boundary witnesses require every available point to be active.
pred ShowFullRouteWithTraffic {
  some s: State |
    sectionInvariant[s] and active[s] = SPC and some inFlight[s]
}

pred ShowFullRouteTransmit {
  some disj a, b: State, m: Message |
    initial[a] and active[a] = SPC and transmit[a, b, m] and
    sectionInvariant[b]
}

pred ShowFullRouteReceive {
  some disj a, b: State |
    sectionInvariant[a] and active[a] = SPC and
    receive[a, b] and sectionInvariant[b]
}

pred ShowFullRouteDaemon {
  some disj a, b: State, p: SPC |
    sectionInvariant[a] and active[a] = SPC and
    daemon[a, b, p] and sectionInvariant[b]
}

pred ShowFullRouteInsertion {
  some disj a, b: State, p, fresh: SPC |
    sectionInvariant[a] and active[a] = SPC - fresh and
    some inFlight[a] and some departed[a, p] and
    insertSection[a, b, p, fresh] and active[b] = SPC and
    sectionInvariant[b]
}

pred ShowFullRoutePendingPoll {
  some disj a, b: State |
    sectionInvariant[a] and active[a] = SPC and some inFlight[a] and
    stutter[a, b] and receivePoll[a, b]
}

// Default exploration: exactly 8 available points, routes using 1..8 points,
// at most 4 message values, four history slots. The Int and seq scopes are
// unused by this encoding; they are kept for runner compatibility.



check InitialIsValid for 4 but 10 SPC, 4 Message, exactly 2 State, 5 Int, 4 seq expect 0
