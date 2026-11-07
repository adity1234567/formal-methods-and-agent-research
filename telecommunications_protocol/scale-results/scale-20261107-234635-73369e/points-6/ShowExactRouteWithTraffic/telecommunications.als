// Generated scaling experiment. Scope below replaces the baseline analysis commands.
module telecommunications

// Original bounded Alloy translation of Woodcock & Davies, Using Z (1996),
// Chapter 20, printed pp.321-329. See README for source and modeling choices.
// Every history is NEWEST FIRST: index 0 is newest; the last item is oldest.
// Message atoms are values: transmitting the same value twice is permitted.
// No global fact assumes sectionInvariant: preservation checks must establish it.

sig Message {}
sig SPC {}

sig State {
  route: seq SPC,
  // Restrict possible indices to this command's sequence bound. Contiguity,
  // ordering, and conservation remain obligations of sectionInvariant.
  rec: SPC -> seq/Int -> lone Message,
  ins: SPC -> seq/Int -> lone Message,
  sent: SPC -> seq/Int -> lone Message
}

fun active[s: State]: set SPC { seq/elems[s.route] }
fun firstPoint[s: State]: lone SPC { seq/first[s.route] }
fun lastPoint[s: State]: lone SPC { seq/last[s.route] }
fun input[s: State]: Int -> Message { s.rec[firstPoint[s]] }
fun output[s: State]: Int -> Message { s.sent[lastPoint[s]] }

// Sequence helpers include length constraints: library insert and append can
// truncate at the finite sequence bound. Truncation is not protocol behavior.
pred concat[a, b, c: Int -> Message] {
  #c = add[#a, #b]
  c = seq/append[a, b]
}

pred prepend[m: Message, pre, post: Int -> Message] {
  #pre < #seq/Int
  #post = add[#pre, 1]
  post = seq/insert[pre, 0, m]
}

pred suffix[whole, ending: Int -> Message] {
  seq/isSeq[whole]
  seq/isSeq[ending]
  #ending <= #whole
  all j: seq/inds[ending] |
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
  seq/isSeq[s.route]
  some s.route
  not seq/hasDups[s.route]
  no (SPC - active[s]).(s.rec + s.ins + s.sent)
  all p: active[s] | {
    seq/isSeq[s.rec[p]]
    seq/isSeq[s.ins[p]]
    seq/isSeq[s.sent[p]]
  }
}

pred sectionInvariant[s: State] {
  shape[s]
  all p: active[s] | concat[s.ins[p], s.sent[p], s.rec[p]]
  all i: seq/inds[s.route] - seq/lastIdx[s.route] |
    s.sent[s.route[i]] = s.rec[s.route[add[i, 1]]]
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
    post.ins[p] = seq/butlast[pre.ins[p]]
    prepend[seq/last[pre.ins[p]], pre.sent[p], post.sent[p]]
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
  let i = seq/idxOf[pre.route, upstream],
      downstream = pre.route[add[i, 1]],
      m = seq/last[pre.ins[upstream]] | {
    post.ins[upstream] = seq/butlast[pre.ins[upstream]]
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

// Section 20.4: insert a fresh signalling point strictly between two points.
// Existing histories stay with their SPC rather than moving numeric indices.
pred insertSection[pre, post: State, upstream, fresh: SPC] {
  upstream in active[pre] - lastPoint[pre]
  fresh not in active[pre]
  #pre.route < #seq/Int
  let i = seq/idxOf[pre.route, upstream],
      downstream = pre.route[add[i, 1]] | {
    post.route = seq/insert[pre.route, add[i, 1], fresh]
    #post.route = add[#pre.route, 1]
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

// Concatenate section buffers in route order. Each position is shifted by
// the lengths of all earlier buffers. Used to check the retrieve theorem.
fun inFlight[s: State]: Int -> Message {
  { k: seq/Int, m: Message |
    some p: active[s], j: seq/inds[s.ins[p]] |
      let offset = (sum q: active[s] |
        seq/idxOf[s.route, q] < seq/idxOf[s.route, p] => #s.ins[q] else 0) |
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
    post.ins[p] = seq/rest[pre.ins[p]]
    prepend[seq/first[pre.ins[p]], pre.sent[p], post.sent[p]]
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
    #input[c] = 2 and #seq/elems[input[c]] = 1 and sectionInvariant[c]
}

// Two different values traverse two sections in FIFO order. Inspect a..g.
pred ShowTwoMessageDelivery {
  some disj a, b, c, d, e, f, g: State, disj m1, m2: Message |
    #a.route = 2 and initial[a] and
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




// Scaling witnesses add scenario constraints, never a global invariant fact.
// They show satisfiability at the active-route boundary, not general reachability.
pred ShowExactRouteWithTraffic {
  some s: State | sectionInvariant[s] and #s.route = 6 and some s.ins
}
pred ShowTransmitAtRouteLimit {
  some disj a,b: State, m: Message |
    #a.route = 6 and initial[a] and transmit[a,b,m] and sectionInvariant[b]
}
pred ShowReceiveAtRouteLimit {
  some disj a,b: State |
    #a.route = 6 and sectionInvariant[a] and receive[a,b] and sectionInvariant[b]
}
pred ShowDaemonAtRouteLimit {
  some disj a,b: State, p: SPC |
    #a.route = 6 and sectionInvariant[a] and daemon[a,b,p] and sectionInvariant[b]
}
pred ShowInsertionAtRouteLimit {
  some disj a,b: State, p,fresh: SPC |
    #a.route = 5 and #b.route = 6 and sectionInvariant[a] and
    some a.ins and insertSection[a,b,p,fresh] and sectionInvariant[b]
}

run ShowExactRouteWithTraffic for 4 but 6 SPC, 4 Message, exactly 1 State, 7 Int, 6 seq expect 1
