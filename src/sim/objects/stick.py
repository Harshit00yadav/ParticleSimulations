def connect(length, par1, par2):
    vect = par1.position - par2.position
    displace = length - vect.magnitude()
    vect = vect.normalize()
    par1.position += vect * (displace / 2)
    par2.position -= vect * (displace / 2)
