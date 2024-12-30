def connect(length, par1, par2, threshold=60):
    vect = par1.position - par2.position
    mag = vect.magnitude()
    displace = length - mag
    if mag > length + threshold:
        vect = vect.normalize()
        par1.position += vect * (displace / 2) * 0.0001
        par2.position -= vect * (displace / 2) * 0.0001
        return False

    vect = vect.normalize()
    par1.position += vect * (displace / 2)
    par2.position -= vect * (displace / 2)
    if mag < length + threshold + threshold/2:
        return True
    return False
