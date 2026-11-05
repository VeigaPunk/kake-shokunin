# Anchor re-check against the retained RFC 9110 body (read-only)

file: .ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt
sha256: 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a
bytes: 502941
command: python3 (hashlib.sha256 over the file bytes; lines split on \n, 1-based)

## S478 §5.6.1.2: lines 1693-1702
```
1693:5.6.1.2.  Recipient Requirements
1694:
1695:   Empty elements do not contribute to the count of elements present.  A
1696:   recipient MUST parse and ignore a reasonable number of empty list
1697:   elements: enough to handle common mistakes by senders that merge
1698:   values, but not so much that they could be used as a denial-of-
1699:   service mechanism.  In other words, a recipient MUST accept lists
1700:   that satisfy the following syntax:
1701:
1702:     #element => [ element ] *( OWS "," OWS [ element ] )
```

## S478 §5.6.3: lines 1745-1745
```
1745:5.6.3.  Whitespace
```

## S478 §5.6.3: lines 1762-1764
```
1762:   OWS and RWS have the same semantics as a single SP.  Any content
1763:   known to be defined as OWS or RWS MAY be replaced with a single SP
1764:   before interpreting it or forwarding the message downstream.
```

## S478 §5.6.3 production: lines 1774-1775
```
1774:     OWS            = *( SP / HTAB )
1775:                    ; optional whitespace
```

## S455 §8.8.3 etagc (context 1584-1588): lines 1584-1588
```
1584:
1585:     field-value    = *field-content
1586:     field-content  = field-vchar
1587:                      [ 1*( SP / HTAB / field-vchar ) field-vchar ]
1588:     field-vchar    = VCHAR / obs-text
```

## S455 obs-text definition §5.5 (not in S455 anchor): lines 1589-1589
```
1589:     obs-text       = %x80-FF
```

## §5.5 trimming (contract C1 context, not an S478 anchor): lines 1591-1591
```
1591:   A field value does not include leading or trailing whitespace.  When
```

## S473 §13.1.2: lines 5872-5932
```
5872:13.1.2.  If-None-Match
5873:
5874:   The "If-None-Match" header field makes the request method conditional
5875:   on a recipient cache or origin server either not having any current
5876:   representation of the target resource, when the field value is "*",
5877:   or having a selected representation with an entity tag that does not
5878:   match any of those listed in the field value.
5879:
5880:   A recipient MUST use the weak comparison function when comparing
5881:   entity tags for If-None-Match (Section 8.8.3.2), since weak entity
5882:   tags can be used for cache validation even if there have been changes
5883:   to the representation data.
5884:
5885:     If-None-Match = "*" / #entity-tag
5886:
5887:   Examples:
5888:
5889:   If-None-Match: "xyzzy"
5890:   If-None-Match: W/"xyzzy"
5891:   If-None-Match: "xyzzy", "r2d2xxxx", "c3piozzzz"
5892:   If-None-Match: W/"xyzzy", W/"r2d2xxxx", W/"c3piozzzz"
5893:   If-None-Match: *
5894:
5895:   If-None-Match is primarily used in conditional GET requests to enable
5896:   efficient updates of cached information with a minimum amount of
5897:   transaction overhead.  When a client desires to update one or more
5898:   stored responses that have entity tags, the client SHOULD generate an
5899:   If-None-Match header field containing a list of those entity tags
5900:   when making a GET request; this allows recipient servers to send a
5901:   304 (Not Modified) response to indicate when one of those stored
5902:   responses matches the selected representation.
5903:
5904:   If-None-Match can also be used with a value of "*" to prevent an
5905:   unsafe request method (e.g., PUT) from inadvertently modifying an
5906:   existing representation of the target resource when the client
5907:   believes that the resource does not have a current representation
5908:   (Section 9.2.1).  This is a variation on the "lost update" problem
5909:   that might arise if more than one client attempts to create an
5910:   initial representation for the target resource.
5911:
5912:   When an origin server receives a request that selects a
5913:   representation and that request includes an If-None-Match header
5914:   field, the origin server MUST evaluate the If-None-Match condition
5915:   per Section 13.2 prior to performing the method.
5916:
5917:   To evaluate a received If-None-Match header field:
5918:
5919:   1.  If the field value is "*", the condition is false if the origin
5920:       server has a current representation for the target resource.
5921:
5922:   2.  If the field value is a list of entity tags, the condition is
5923:       false if one of the listed tags matches the entity tag of the
5924:       selected representation.
5925:
5926:   3.  Otherwise, the condition is true.
5927:
5928:   An origin server that evaluates an If-None-Match condition MUST NOT
5929:   perform the requested method if the condition evaluates to false;
5930:   instead, the origin server MUST respond with either a) the 304 (Not
5931:   Modified) status code if the request method is GET or HEAD or b) the
5932:   412 (Precondition Failed) status code for all other request methods.
```

## S474 §13.1.3: lines 5942-6022
```
5942:13.1.3.  If-Modified-Since
5943:
5944:   The "If-Modified-Since" header field makes a GET or HEAD request
5945:   method conditional on the selected representation's modification date
5946:   being more recent than the date provided in the field value.
5947:   Transfer of the selected representation's data is avoided if that
5948:   data has not changed.
5949:
5950:     If-Modified-Since = HTTP-date
5951:
5952:   An example of the field is:
5953:
5954:   If-Modified-Since: Sat, 29 Oct 1994 19:43:31 GMT
5955:
5956:   A recipient MUST ignore If-Modified-Since if the request contains an
5957:   If-None-Match header field; the condition in If-None-Match is
5958:   considered to be a more accurate replacement for the condition in If-
5959:   Modified-Since, and the two are only combined for the sake of
5960:   interoperating with older intermediaries that might not implement
5961:   If-None-Match.
5962:
5963:   A recipient MUST ignore the If-Modified-Since header field if the
5964:   received field value is not a valid HTTP-date, the field value has
5965:   more than one member, or if the request method is neither GET nor
5966:   HEAD.
5967:
5968:   A recipient MUST ignore the If-Modified-Since header field if the
5969:   resource does not have a modification date available.
5970:
5971:   A recipient MUST interpret an If-Modified-Since field value's
5972:   timestamp in terms of the origin server's clock.
5973:
5974:   If-Modified-Since is typically used for two distinct purposes: 1) to
5975:   allow efficient updates of a cached representation that does not have
5976:   an entity tag and 2) to limit the scope of a web traversal to
5977:   resources that have recently changed.
5978:
5979:   When used for cache updates, a cache will typically use the value of
5980:   the cached message's Last-Modified header field to generate the field
5981:   value of If-Modified-Since.  This behavior is most interoperable for
5982:   cases where clocks are poorly synchronized or when the server has
5983:   chosen to only honor exact timestamp matches (due to a problem with
5984:   Last-Modified dates that appear to go "back in time" when the origin
5985:   server's clock is corrected or a representation is restored from an
5986:   archived backup).  However, caches occasionally generate the field
5987:   value based on other data, such as the Date header field of the
5988:   cached message or the clock time at which the message was received,
5989:   particularly when the cached message does not contain a Last-Modified
5990:   header field.
5991:
5992:   When used for limiting the scope of retrieval to a recent time
5993:   window, a user agent will generate an If-Modified-Since field value
5994:   based on either its own clock or a Date header field received from
5995:   the server in a prior response.  Origin servers that choose an exact
5996:   timestamp match based on the selected representation's Last-Modified
5997:   header field will not be able to help the user agent limit its data
5998:   transfers to only those changed during the specified window.
5999:
6000:   When an origin server receives a request that selects a
6001:   representation and that request includes an If-Modified-Since header
6002:   field without an If-None-Match header field, the origin server SHOULD
6003:   evaluate the If-Modified-Since condition per Section 13.2 prior to
6004:   performing the method.
6005:
6006:   To evaluate a received If-Modified-Since header field:
6007:
6008:   1.  If the selected representation's last modification date is
6009:       earlier or equal to the date provided in the field value, the
6010:       condition is false.
6011:
6012:   2.  Otherwise, the condition is true.
6013:
6014:   An origin server that evaluates an If-Modified-Since condition SHOULD
6015:   NOT perform the requested method if the condition evaluates to false;
6016:   instead, the origin server SHOULD generate a 304 (Not Modified)
6017:   response, including only those metadata that are useful for
6018:   identifying or updating a previously cached response.
6019:
6020:   Requirements on cache handling of a received If-Modified-Since header
6021:   field are defined in Section 4.3.2 of [CACHING].
6022:
```

## S474 §13.1.4: lines 6023-6075
```
6023:13.1.4.  If-Unmodified-Since
6024:
6025:   The "If-Unmodified-Since" header field makes the request method
6026:   conditional on the selected representation's last modification date
6027:   being earlier than or equal to the date provided in the field value.
6028:   This field accomplishes the same purpose as If-Match for cases where
6029:   the user agent does not have an entity tag for the representation.
6030:
6031:     If-Unmodified-Since = HTTP-date
6032:
6033:   An example of the field is:
6034:
6035:   If-Unmodified-Since: Sat, 29 Oct 1994 19:43:31 GMT
6036:
6037:   A recipient MUST ignore If-Unmodified-Since if the request contains
6038:   an If-Match header field; the condition in If-Match is considered to
6039:   be a more accurate replacement for the condition in If-Unmodified-
6040:   Since, and the two are only combined for the sake of interoperating
6041:   with older intermediaries that might not implement If-Match.
6042:
6043:   A recipient MUST ignore the If-Unmodified-Since header field if the
6044:   received field value is not a valid HTTP-date (including when the
6045:   field value appears to be a list of dates).
6046:
6047:   A recipient MUST ignore the If-Unmodified-Since header field if the
6048:   resource does not have a modification date available.
6049:
6050:   A recipient MUST interpret an If-Unmodified-Since field value's
6051:   timestamp in terms of the origin server's clock.
6052:
6053:   If-Unmodified-Since is most often used with state-changing methods
6054:   (e.g., POST, PUT, DELETE) to prevent accidental overwrites when
6055:   multiple user agents might be acting in parallel on a resource that
6056:   does not supply entity tags with its representations (i.e., to
6057:   prevent the "lost update" problem).  In general, it can be used with
6058:   any method that involves the selection or modification of a
6059:   representation to abort the request if the selected representation's
6060:   last modification date has changed since the date provided in the If-
6061:   Unmodified-Since field value.
6062:
6063:   When an origin server receives a request that selects a
6064:   representation and that request includes an If-Unmodified-Since
6065:   header field without an If-Match header field, the origin server MUST
6066:   evaluate the If-Unmodified-Since condition per Section 13.2 prior to
6067:   performing the method.
6068:
6069:   To evaluate a received If-Unmodified-Since header field:
6070:
6071:   1.  If the selected representation's last modification date is
6072:       earlier than or equal to the date provided in the field value,
6073:       the condition is true.
6074:
6075:   2.  Otherwise, the condition is false.
```
