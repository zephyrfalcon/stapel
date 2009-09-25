# standard library for Stapel ^_^

# ( a b c -- a b b c )
:dupd ( ( dup ) dip ) define

# ( a b c -- b a c )
:swapd ( ( swap ) dip ) define

# ++: add one to a variable.
:++ ( # symbol --
    dup                         # symbol symbol
    ref                         # symbol value-of-symbol
    1 +                         # symbol value+1
    define                      # store the new value
) define

:if ( # cond trueblock falseblock -- 
    choice exec
) define

:map ( # block list -- transformed-list
    [ ] ror             # accum block list
    map-aux
) define

# works! ^_^
:map-aux ( # accum block list -- transformed-list
    dup                      # accum block list list
    empty?                   # accum block list bool
    ( drop drop )            # accum [done now]
    (
        uncons               # accum block head tail
        (                    # accum block head
            swap             # accum head block
            dup              # accum head block block
            (                # accum head block
                exec         # accum new-value
                append       # accum+value
            ) dip            # accum+value block
        ) dip                # accum+value block tail
        map-aux
    ) 
    if
) define

:filter ( # block list -- filtered-list
    [ ] ror filter-aux
) define

# untested
:filter-aux ( # accum block list -- filtered-list
    dup                         # accum block list list
    empty?                      # accum block list bool
    ( drop drop )               # accum [done now]
    (
        uncons                  # accum block head tail
        (                       # accum block head
            swap                # accum head block
            dup                 # accum head block block
            (                   # accum head block
                dupd            # accum head head block
                exec            # accum head bool
                ( append )      # accum+head
                ( drop )        # accum
                if
            ) dip
        ) dip
        filter-aux
    )
    if
) define
