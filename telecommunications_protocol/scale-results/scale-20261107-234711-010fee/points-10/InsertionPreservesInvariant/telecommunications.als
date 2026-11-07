// Generated scaling experiment. Scope below replaces the baseline analysis commands.
module telecommunications_scalable

open util/ordering[SPC] as pointOrder
open util/sequniv as seqLib

// Scalable representation of the telecommunications case study in Using Z,
// Chapter 20. See scaling_design.md for the representation correspondence.
// A fixed ordered point pool supplies route order; each State selects its
// active subsequence. Point scope and message-history length are independent.
// util/ordering makes the SPC pool scope EXACT, while active routes may use
// any nonempty subset. No global fact assumes validity of sectional states.
// Every history is NEWEST FIRST: index 0 is newest; the last item is oldest.
// Message atoms are values: transmitting the same value twice is permitted.
// No global fact assumes sectionInvariant: preservation checks must establish it.

sig Message {}
sig SPC {}

sig State {
  route: set SPC,
  // Restrict possible indices to this command's sequence bound. Contiguity,
  // ordering, and conservation remain obligations of sectionInvariant.
  rec: SPC -> seq/Int -> lone Message,
  ins: SPC -> seq/Int -> lone Message,
  sent: SPC -> seq/Int -> lone Message
}

fun active[s: State]: set SPC { s.route }
fun firstPoint[s: State]: lone SPC { pointOrder/min[s.route] }
fun lastPoint[s: State]: lone SPC { pointOrder/max[s.route] }
fun nextPoint[s: State, p: SPC]: lone SPC {
  pointOrder/min[s.route & pointOrder/nexts[p]]
}
fun input[s: State]: Int -> Message { s.rec[firstPoint[s]] }
fun output[s: State]: Int -> Message { s.sent[lastPoint[s]] }

// Sequence helpers include length constraints: library insert and append can
// truncate at the finite sequence bound. Truncation is not protocol behavior.
pred concat[a, b, c: Int -> Message] {
  #c = add[#a, #b]
  c = seqLib/append[a, b]
}

pred prepend[m: Message, pre, post: Int -> Message] {
  #pre < #seq/Int
  #post = add[#pre, 1]
  post = seqLib/insert[pre, 0, m]
}

pred suffix[whole, ending: Int -> Message] {
  seqLib/isSeq[whole]
  seqLib/isSeq[ending]
  #ending <= #whole
  all j: seqLib/inds[ending] |
    ending[j] = whole[add[sub[#whole, #ending], j]]
}

// Ext: output must be a suffix because newest messages are on the left.
pred externalInvariant[incoming, outgoing: Int -> Message] {
  suffix[incoming, outgoing]
}

pred externalTransmit[beforeIn, beforeOut, afterIn, afterOut: Int -> Message,
                      m: Message] {
  externalInvariant[beforeIn, beforeOut]
  externalInvariant[afterIn, afterOut]
  prepend[m, beforeIn, afterIn]
  afterOut = beforeOut
}

// The book's Receive permits stuttering even when messages are pending.
pred externalReceive[beforeIn, beforeOut, afterIn, afterOut: Int -> Message] {
  externalInvariant[beforeIn, beforeOut]
  externalInvariant[afterIn, afterOut]
  afterIn = beforeIn
  (#afterOut = add[#beforeOut, 1] or afterOut = beforeOut)
}

pred shape[s: State] {
  some s.route
  no (SPC - active[s]).(s.rec + s.ins + s.sent)
  all p: active[s] | {
    seqLib/isSeq[s.rec[p]]
    seqLib/isSeq[s.ins[p]]
    seqLib/isSeq[s.sent[p]]
  }
}

pred sectionInvariant[s: State] {
  shape[s]
  all p: active[s] | concat[s.ins[p], s.sent[p], s.rec[p]]
  all p: active[s] - lastPoint[s] |
    s.sent[p] = s.rec[nextPoint[s, p]]
}

pred initial[s: State] {
  shape[s]
  no s.rec + s.ins + s.sent
}

// STransmit. All sections other than the first retain their histories.
pred transmit[pre, post: State, m: Message] {
  post.route = pre.route
  let p = firstPoint[pre] | {
    prepend[m, pre.rec[p], post.rec[p]]
    prepend[m, pre.ins[p], post.ins[p]]
    all q: SPC - p | {
      post.rec[q] = pre.rec[q]
      post.ins[q] = pre.ins[q]
    }
  }
  post.sent = pre.sent
}

// Successful SReceive. Empty final buffers disable this predicate, as the
// chapter's last(last ins) is undefined on an empty sequence.
pred receive[pre, post: State] {
  post.route = pre.route
  post.rec = pre.rec
  let p = lastPoint[pre] | {
    some pre.ins[p]
    post.ins[p] = seqLib/butlast[pre.ins[p]]
    prepend[seqLib/last[pre.ins[p]], pre.sent[p], post.sent[p]]
    all q: SPC - p | {
      post.ins[q] = pre.ins[q]
      post.sent[q] = pre.sent[q]
    }
  }
}

// Successful Daemon0. The oldest message is removed from the upstream buffer
// and prepended downstream. Updating the two boundary histories makes their
// consistency explicit rather than relying on a post-state invariant.
pred daemon[pre, post: State, upstream: SPC] {
  upstream in active[pre] - lastPoint[pre]
  some pre.ins[upstream]
  post.route = pre.route
  let downstream = nextPoint[pre, upstream],
      m = seqLib/last[pre.ins[upstream]] | {
    post.ins[upstream] = seqLib/butlast[pre.ins[upstream]]
    prepend[m, pre.sent[upstream], post.sent[upstream]]
    prepend[m, pre.ins[downstream], post.ins[downstream]]
    prepend[m, pre.rec[downstream], post.rec[downstream]]
    post.rec[upstream] = pre.rec[upstream]
    post.sent[downstream] = pre.sent[downstream]
    all q: SPC - upstream - downstream | {
      post.rec[q] = pre.rec[q]
      post.ins[q] = pre.ins[q]
      post.sent[q] = pre.sent[q]
    }
  }
}

pred stutter[pre, post: State] {
  post.route = pre.route
  post.rec = pre.rec
  post.ins = pre.ins
  post.sent = pre.sent
}

// Explicit implementation choice beyond the successful schema: a polling
// receive can return without delivery at any time, matching abstract Receive.
pred receivePoll[pre, post: State] {
  receive[pre, post] or stutter[pre, post]
}

pred daemonOrIdle[pre, post: State] {
  (some p: SPC | daemon[pre, post, p]) or stutter[pre, post]
}

// Section 20.4: activate a fresh point between existing neighbors.
// Its position in the ordered pool must lie inside the chosen gap. This is
// a representation condition, not an additional condition on message traffic.
// Existing histories stay with their SPC. See the enabledness caveat in
// scaling_design.md: inactive pool positions form part of this representation.
pred insertSection[pre, post: State, upstream, fresh: SPC] {
  upstream in active[pre] - lastPoint[pre]
  fresh not in active[pre]
  let downstream = nextPoint[pre, upstream] | {
    fresh in pointOrder/nexts[upstream] & pointOrder/prevs[downstream]
    post.route = pre.route + fresh
    post.rec[fresh] = pre.sent[upstream]
    no post.ins[fresh]
    post.sent[fresh] = pre.rec[downstream]
    all q: SPC - fresh | {
      post.rec[q] = pre.rec[q]
      post.ins[q] = pre.ins[q]
      post.sent[q] = pre.sent[q]
    }
  }
}

// On sectional-invariant states, local conservation telescopes:
//   sum(lengths of earlier pending queues) = #input - #rec[p].
// Use that offset instead of a sum over all preceding points. The returned
// values still come from pending queues, not from the desired retrieve result.
// Outside valid states, this function need not be route-order concatenation.
// Length arithmetic remains bounded by the history bound, independently of N.
fun inFlight[s: State]: Int -> Message {
  { k: seq/Int, m: Message |
    some p: active[s], j: seqLib/inds[s.ins[p]] |
      let offset = sub[#input[s], #s.rec[p]] |
        k = add[offset, j] and m = s.ins[p][j]
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
// No correct operation, trace, or other assertion calls this predicate.
pred receiveNewestFirst_BUG[pre, post: State] {
  post.route = pre.route
  post.rec = pre.rec
  let p = lastPoint[pre] | {
    some pre.ins[p]
    post.ins[p] = seqLib/rest[pre.ins[p]]
    prepend[seqLib/first[pre.ins[p]], pre.sent[p], post.sent[p]]
    all q: SPC - p | {
      post.ins[q] = pre.ins[q]
      post.sent[q] = pre.sent[q]
    }
  }
}

// EXPECTED TO FAIL: Alloy should produce a counterexample with two different
// pending values, showing why removing the oldest value is essential.
assert BrokenReceiveWouldPreserveInvariant {
  all pre, post: State |
    (sectionInvariant[pre] and receiveNewestFirst_BUG[pre, post]) implies
      sectionInvariant[post]
}

// Witnesses are important: universal assertions can pass vacuously if no
// operation can run. Each successful operation has its own satisfiable run.
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
    // Exercise both pending traffic and a nonempty inherited boundary history.
    sectionInvariant[a] and some inFlight[a] and some a.sent[p] and
    insertSection[a, b, p, fresh] and sectionInvariant[b]
}

pred ShowRepeatedMessageValue {
  some disj a, b, c: State, m: Message |
    initial[a] and transmit[a, b, m] and transmit[b, c, m] and
    #input[c] = 2 and #seqLib/elems[input[c]] = 1 and sectionInvariant[c]
}

// Two different values traverse two sections in FIFO order. Inspect a..g.
pred ShowTwoMessageDelivery {
  some disj a, b, c, d, e, f, g: State, disj m1, m2: Message |
    (some disj p, q: SPC | a.route = p + q) and initial[a] and
    transmit[a, b, m1] and transmit[b, c, m2] and
    daemon[c, d, firstPoint[c]] and daemon[d, e, firstPoint[d]] and
    receive[e, f] and receive[f, g] and
    sectionInvariant[g] and
    output[f] = 0 -> m1 and output[g] = (0 -> m2 + 1 -> m1) and
    no inFlight[g]
}

// This witness makes the absence of a delivery guarantee explicit: an input
// can remain pending across a polling receive that does no work.
pred ShowPendingPollCanStutter {
  some disj a, b: State |
    sectionInvariant[a] and some inFlight[a] and
    stutter[a, b] and receivePoll[a, b]
}


// Boundary witnesses require every available point to be active. They avoid
// cardinality arithmetic on the route so network size does not inflate Int.
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
    some inFlight[a] and some a.sent[p] and
    insertSection[a, b, p, fresh] and active[b] = SPC and
    sectionInvariant[b]
}

pred ShowFullRoutePendingPoll {
  some disj a, b: State |
    sectionInvariant[a] and active[a] = SPC and some inFlight[a] and
    stutter[a, b] and receivePoll[a, b]
}

// Default exploration: exactly 8 available points, routes using 1..8 points,
// at most 4 message values, histories <=4, signed 5-bit integers.
// These command declarations are analysis requests, not claims of completion.



check InsertionPreservesInvariant for 4 but 10 SPC, 4 Message, exactly 2 State, 5 Int, 4 seq expect 0
