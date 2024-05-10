"""

Module with functions to generate BOSS software inputs (ZMAT)

Author: Israel Cabeza de Vaca Lopez
Email:  israel.cabezadevaca@icm.uu.se

"""


from os import path

import logging
logger = logging.getLogger(__name__)

def getFileNames(molname, workdir):
    """
    Get File name of the Zmat 

    Parameters
    ----------
    molname : str
        Molecule name
    workdir : str
        Working folder

    Returns
    -------
    str
        Zmat file name
    """

    return path.join(workdir, molname+".z")


def getFileNamesDual(molname, workdir):

    return path.join(workdir, molname+"_dual.z")


def write(molecule, molname, workdir, writeAtomParameters = False):
    """
    Write a molecule object in a file using the zmat format (BOSS input format)

    Parameters
    ----------
    molecule : Molecule object
        Molecule object from the input
    molname : str
        Molecule name
    workdir : str
        Working folder path
    writeAtomParameters : bool, optional
        If True, charges and VdW parameters are printed too, by default False
    """

    if logger!=None: logger.info('Generating Zmat')

    ofileName = getFileNames(molname, workdir) 

    with open(ofileName,'w') as ofile:

        ofile.write('BOSS ZMAT generated by LigParGen2.1 (israel.cabezadevaca@yale.edu) \n')

        for atom in molecule.atoms: 
            
            ofile.write('%4d %-3s%5d%5d%5d%12.6f%4d%12.6f%4d%12.6f%4s%5d\n' % (int(atom.serial), atom.name, \
                int(atom.typeA), int(atom.typeB), atom.parent,atom.r, atom.parentParent, atom.angle, atom.parentParentParent, \
                atom.dihedral, molecule.residueName, atom.resnum))

        ofile.write('                    Geometry Variations follow    (2I4,F12.6)\n')

        for geometry in molecule.geometryVariations: ofile.write(geometry)

        ofile.write('                    Variable Bonds follow         (I4)\n')

        for bond in molecule.bondsVariable: ofile.write('%4d                            \n' % (bond.atomA.serial))

        ofile.write('                    Additional Bonds follow       (2I4)\n')

        for bond in molecule.bondsAdditional: ofile.write('%4d%4d                        \n' % (bond.atomA.serial,bond.atomB.serial))

        ofile.write('''                    Harmonic Constraints follow   (2I4,4F10.4)
                    Variable Bond Angles follow   (I4)\n''')

        for angle in molecule.anglesVariable: ofile.write('%4d                         \n' % (angle.atomA.serial))

        ofile.write('                    Additional Bond Angles follow (3I4)\n')

        for angle in molecule.anglesAdditional: ofile.write('%4d%4d%4d                               \n' % (angle.atomA.serial,angle.atomB.serial,angle.atomC.serial))

        ofile.write('                    Variable Dihedrals follow     (3I4,F12.6)\n')

        for dihedral in molecule.torsionsVariable: ofile.write('%4d%4d%4d%12.6f                         \n' % (dihedral.atomA.serial, \
            dihedral.typeInitial, dihedral.typeFinal, dihedral.displacement))

        ofile.write('                    Additional Dihedrals follow   (6I4)\n')

        for dihedral in molecule.torsionsAdditional: ofile.write('%4d%4d%4d%4d%4d%4d                       \n' % (dihedral.atomA.serial, dihedral.atomB.serial, 
                dihedral.atomC.serial, dihedral.atomD.serial, dihedral.typeInitial, dihedral.typeFinal))

        ofile.write('                    Domain Definitions follow     (4I4)\n')

        for excluded in molecule.excludedList: ofile.write('%4d%4d%4d%4d                                \n' % (excluded[0], excluded[1], excluded[2], excluded[3]))

        ofile.write(
            '''                    Conformational Search (2I4,2F12.6)
                    Local Heating Residues follow (I4 or I4-I4)
                    Final blank line         
                                                                         
                                                                 
 Final Non-Bonded Parameters for QM (AM1 CM1Lx1.14) Atoms:               
                  
''')

        if writeAtomParameters:

            atomsWithNonbondedParameters= [atom for atom in molecule.atoms if atom.typeA!=-1]

            for atom in atomsWithNonbondedParameters:
                if atom.typeA !=100:

                    ofile.write('%4d%3d%3s%11.6f%10.6f%10.6f                              \n' % (atom.typeA, atom.atomicNumber, atom.atomTypeOPLS, atom.charge, atom.sigma, atom.epsilon)) 

            for atom in atomsWithNonbondedParameters:
                if atom.typeA !=atom.typeB and atom.typeB!=100:
                    
                    ofile.write('%4d%3d%3s%11.6f%10.6f%10.6f                                \n' % (atom.typeB, atom.atomicNumber_B, atom.atomTypeOPLS_B, atom.charge_B, atom.sigma_B, atom.epsilon_B))


        ofile.write('                      \n')

    return ofileName

