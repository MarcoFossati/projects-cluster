// Magnetostatics.pro
//
// Magnetostatics - magnetic scalar potential (phi) and magnetic vector (a)
// formulations
//
// You can either merge this file in an other problem description file (see
// e.g. getdp/demos/magnet.pro), or open the file with Gmsh along with a
// geometry: you will then be prompted to setup your materials and boundary
// conditions for each physical group, interactively.

DefineConstant[
  formulationType = {1, Choices{0="Scalar potential", 1="Vector potential"},
    Help Str[
      "Magnetostatic model definitions",
      "h: magnetic field [A/m]",
      "b: magnetic flux density [T]",
      "phi: scalar magnetic potential (h = -grad phi) [A]",
      "a: vector magnetic potential (b = curl a) [T.m]"],
    Name "GetDP/Formulation"},
  modelPath = GetString["Gmsh/Model absolute path"],
  resPath = StrCat[modelPath, "res/"],
  exportFile = StrCat[modelPath, "export.pro"]
];

Group {
  // generic groups needed by the model
  DefineGroup[
    Domain_M, // magnets
    Domain_S, // imposed current density
    Domain_Inf, // infinite domains
    Domain_NL, // nonlinear magnetic materials
    Domain_Mag, // linear magnetic materials
    Domain_Dirichlet // Dirichlet boundary conditions
  ];

  // interactive model setup if no region currently defined
  interactive = !NbrRegions[];
  export = !StrCmp[OnelabAction, "compute"];
  modelDim = GetNumber["Gmsh/Model dimension"];
  numPhysicals = GetNumber["Gmsh/Number of physical groups"];

  // interactive construction of groups with Gmsh
  If(interactive)
    If(export)
      Printf('Group{') > Str[exportFile];
    EndIf
    For i In {1:numPhysicals}
      dim~{i} = GetNumber[Sprintf["Gmsh/Physical group %g/Dimension", i]];
      name~{i} = GetString[Sprintf["Gmsh/Physical group %g/Name", i]];
      tag~{i} = GetNumber[Sprintf["Gmsh/Physical group %g/Number", i]];
      reg = Sprintf["Region[%g]; ", tag~{i}]; str = "";
      If(dim~{i} < modelDim)
        DefineConstant[
          bc~{i} = {0, ReadOnlyRange 1, Choices{
              0=StrCat["Neumann: zero ", StrChoice[formulationType, "h.t", "b.n"]],
              1=StrCat["Dirichlet: fixed ", StrChoice[formulationType, "b.n", "h.t"]]
            },
            Name StrCat["Parameters/Boundary conditions/", name~{i}, "/0Type"]}
        ];
        If(bc~{i} == 1)
          str = StrCat["Domain_Dirichlet += ", reg];
        EndIf
      Else
        DefineConstant[
          material~{i} = {2, Choices{
              0="Magnet",
              1="Current source",
              2="Linear magnetic material",
              3="Nonlinear magnetic material",
              4="Infinite air shell"
            },
            Name StrCat["Parameters/Materials/", name~{i}, "/0Type"]}
        ];
        If(material~{i} == 0)
          str = StrCat["Domain_M += ", reg];
        ElseIf(material~{i} == 1)
          str = StrCat["Domain_S += ", reg];
        ElseIf(material~{i} == 2)
          str = StrCat["Domain_Mag += ", reg];
        ElseIf(material~{i} == 3)
          str = StrCat["Domain_NL += ", reg];
        ElseIf(material~{i} == 4)
          str = StrCat["Domain_Inf += ", reg];
        EndIf
      EndIf
      Parse[str];
      If(export && StrLen[str])
        Printf(Str[str]) >> Str[exportFile];
      EndIf
    EndFor
    If(export)
      Printf('}') >> Str[exportFile];
    EndIf
  EndIf

  Domain = Region[{Domain_Mag, Domain_NL, Domain_M, Domain_S, Domain_Inf}];
}

If(interactive)
  Include "MaterialDatabase.pro";
  If(export)
    Printf('Include "MaterialDatabase.pro";') >> Str[exportFile];
  EndIf
EndIf

Function{
  // generic functions needed by the model
  DefineFunction[
    mu, // magnetic permeability
    nu, // magnetic reluctivity (= 1/nu)
    hc, // coercive magnetic field (in magnets)
    js, // source current density
    dhdb_NL, dbdh_NL // nonlinear parts of the Jacobian
  ];

  // definition of these function in interactive mode
  If(interactive)
    If(export)
      Printf('Function {') >> Str[exportFile];
    EndIf
    For i In {1:numPhysicals}
      If(dim~{i} < modelDim)
        DefineConstant[
          bc_val~{i} = {0., Visible bc~{i},
            Name StrCat["Parameters/Boundary conditions/", name~{i}, "/1Value"]}
        ];
      Else
        DefineConstant[
          hc_preset~{i} = {#permanentMagnetMaterials() > 2 ? 2 : 0,
            Visible (material~{i} == 0),
            Choices{ 0:#permanentMagnetMaterials()-1 = permanentMagnetMaterials() },
            Name StrCat["Parameters/Materials/", name~{i}, "/1hc preset"],
            Label "Choice"},
          hcx~{i} = {920000, Visible (material~{i} == 0 && hc_preset~{i} == 0),
            Name StrCat["Parameters/Materials/", name~{i}, "/hcx value"],
            Label "h_cx [A/m]", Help "Coercive magnetic field along x-axis"},
          hcy~{i} = {0, Visible (material~{i} == 0 && hc_preset~{i} == 0),
            Name StrCat["Parameters/Materials/", name~{i}, "/hcy value"],
            Label "h_cy [A/m]", Help "Coercive magnetic field along y-axis"},
          hcz~{i} = {0, Visible (material~{i} == 0 && hc_preset~{i} == 0 && dim~{i} == 3),
            Name StrCat["Parameters/Materials/", name~{i}, "/hcz value"],
            Label "h_cz [A/m]", Help "Coercive magnetic field along z-axis"},
          hc_fct~{i} = {"Vector[92000, 0, 0]",
            Visible (material~{i} == 0 && hc_preset~{i} == 1),
            Name StrCat["Parameters/Materials/", name~{i}, "/hc function"],
            Label "h_c [A/m]", Help "Coercive magnetic field"},
          js_preset~{i} = {0, Visible (material~{i} == 1),
            Choices{ 0="Constant", 1="Function" },
            Name StrCat["Parameters/Materials/", name~{i}, "/1js preset"],
            Label "Choice"},
          jsx~{i} = {0, Visible (material~{i} == 1 && js_preset~{i} == 0 && dim~{i} == 3),
            Name StrCat["Parameters/Materials/", name~{i}, "/jx value"],
            Label "j_sx [A/m²]", Help "Current density along x-axis"},
          jsy~{i} = {0, Visible (material~{i} == 1 && js_preset~{i} == 0&& dim~{i} == 3),
            Name StrCat["Parameters/Materials/", name~{i}, "/jy value"],
            Label "j_sy [A/m²]", Help "Current density along y-axis"},
          jsz~{i} = {1, Visible (material~{i} == 1 && js_preset~{i} == 0),
            Name StrCat["Parameters/Materials/", name~{i}, "/jz value"],
            Label "j_sz [A/m²]", Help "Current density along z-axis"},
          js_fct~{i} = {"Vector[0, 0, 1]",
            Visible (material~{i} == 1 && js_preset~{i} == 1),
            Name StrCat["Parameters/Materials/", name~{i}, "/js function"],
            Label "j_s [A/m²]", Help "Current density"},
          mur_preset~{i} = {#linearMagneticMaterials() > 2 ? 2 : 0,
            Visible (material~{i} == 2),
            Choices{ 0:#linearMagneticMaterials()-1 = linearMagneticMaterials() },
            Name StrCat["Parameters/Materials/", name~{i}, "/1mur preset"],
            Label "Choice"}
          mur~{i} = {1, Visible (material~{i} == 2 && mur_preset~{i} == 0),
            Name StrCat["Parameters/Materials/", name~{i}, "/mur value"],
            Label "μ_r", Help "Relative magnetic permeability"},
          mur_fct~{i} = {"1", Visible (material~{i} == 2 && mur_preset~{i} == 1),
            Name StrCat["Parameters/Materials/", name~{i}, "/mur function"],
            Label "μ_r", Help "Relative magnetic permeability"},
          bh_preset~{i} = {#nonlinearMagneticMaterials() > 2 ? 2 : 0,
            Visible (material~{i} == 3),
            Choices{ 0:#nonlinearMagneticMaterials()-1 = nonlinearMagneticMaterials() },
            Name StrCat["Parameters/Materials/", name~{i}, "/1bh preset"],
            Label "Choice"}
          b_list~{i} = {"{0,0.3,0.7,1,1.4,1.7,2.2}",
            Visible (material~{i} == 3 && bh_preset~{i} == 0),
            Name StrCat["Parameters/Materials/", name~{i}, "/3b values"]},
          h_list~{i} = {"{0,30,90,2e2,6e2,4e3,7e5}",
            Visible (material~{i} == 3 && bh_preset~{i} == 0),
            Name StrCat["Parameters/Materials/", name~{i}, "/2h values"]},
          nu_fct~{i} = {"100. + 10. * Exp[1.8*SquNorm[$1]]",
            Visible (material~{i} == 3 && bh_preset~{i} == 1),
            Name StrCat["Parameters/Materials/", name~{i}, "/2nu function"],
            Label "ν(b) [m/H]", Help "Magnetic reluctivity"},
          dnudb2_fct~{i} = {"18. * Exp[1.8*SquNorm[$1]]",
            Visible (material~{i} == 3 && bh_preset~{i} == 1),
            Name StrCat["Parameters/Materials/", name~{i}, "/3dnudb2 function"],
            Label "dν/db²"},
          mu_fct~{i} = {"***", Visible (material~{i} == 3 && bh_preset~{i} == 1),
            Name StrCat["Parameters/Materials/", name~{i}, "/4mu function"],
            Label "μ(h) [H/m]", Help "Magnetic permeability"},
          dmudh2_fct~{i} = {"***", Visible (material~{i} == 3 && bh_preset~{i} == 1),
            Name StrCat["Parameters/Materials/", name~{i}, "/5dmudh2 function"],
            Label "dμ/dh²"}
        ];
        reg = Sprintf["[Region[%g]]", tag~{i}]; str = ""; str2 = "";
        If(material~{i} == 0 && hc_preset~{i} == 0) // magnet, constant
          str = StrCat["hc", reg, Sprintf[" = Vector[%g, %g, %g]; ", hcx~{i},
            hcy~{i}, hcz~{i}], "mu", reg, " = mu0; ", "nu", reg, " = 1/mu0; "];
        ElseIf(material~{i} == 0 && hc_preset~{i} == 1) // magnet, function
          str = StrCat["hc", reg, " = ", hc_fct~{i}, "; ", "mu", reg, " = mu0; ",
            "nu", reg, " = 1/mu0; "];
        ElseIf(material~{i} == 0 && hc_preset~{i} > 1) // magnet, preset
          n = Str[ permanentMagnetMaterials(hc_preset~{i}) ];
          str = StrCat["hc", reg, " = ", n, "_hc; ", "mu", reg, " = ", n,
            "_mur*mu0; ", "nu", reg, " = 1/(", n, "_mur*mu0); "];
        ElseIf(material~{i} == 1 && js_preset~{i} == 0) // current source, constant
          str = StrCat["js", reg, " = ", Sprintf["Vector[%g, %g, %g]; ", jsx~{i},
            jsy~{i}, jsz~{i}], "mu", reg, " = mu0; ", "nu", reg, " = 1/mu0; "];
        ElseIf(material~{i} == 1 && js_preset~{i} == 1) // current source, function
          str = StrCat["js", reg, " = ", js_fct~{i}, "; ", "mu", reg, " = mu0; ",
            "nu", reg, " = 1/mu0; "];
        ElseIf(material~{i} == 2 && mur_preset~{i} == 0) // linear material, constant
          str = StrCat["mu", reg, " = ", Sprintf["%g", mur~{i}], "*mu0; ",
            "nu", reg, " = 1/(", Sprintf["%g", mur~{i}], "*mu0); "];
        ElseIf(material~{i} == 2 && mur_preset~{i} == 1) // linear material, function
          str = StrCat["mu", reg, " = (", mur_fct~{i}, ")*mu0; ", "nu", reg,
            " = 1/((", mur_fct~{i}, ")*mu0); "];
        ElseIf(material~{i} == 2 && mur_preset~{i} > 1) // linear material, preset
          n = Str[ linearMagneticMaterials(mur_preset~{i}) ];
          str = StrCat["mu", reg, " = ", n, "_mur*mu0; ", "nu", reg, " = 1/(",
            n, "_mur*mu0); "];
        ElseIf(material~{i} == 3) // nonlinear material
          If(bh_preset~{i} == 0) // data points
            n = Sprintf["UserMaterialPts_%g", i];
            str = StrCat[n, "_b_list() = ", b_list~{i}, "; ", n, "_h_list() = ",
              h_list~{i}, "; ", "_MaterialName_ = '", n,
              "'; Call DefineMaterialFunctions; "];
          ElseIf(bh_preset~{i} == 1) // function
            n = Sprintf["UserMaterialFct_%g", i];
            str = StrCat[n, "_nu[] = ", nu_fct~{i}, "; ", n, "_dnudb2[] = ",
              dnudb2_fct~{i}, "; ", n, "_mu[] = ", nu_fct~{i}, "; ", n,
              "_dmudh2[] = ", dnudb2_fct~{i}, "; ", "_MaterialName_ = '", n,
              "'; Call DefineMaterialFunctions; "];
          Else // preset
            n = Str[ nonlinearMagneticMaterials(bh_preset~{i}) ];
          EndIf
          str2 = StrCat["mu", reg, " = ", n, "_mu[$1]; ", "dbdh_NL", reg, " = ",
            n, "_dbdh_NL[$1]; ", "nu", reg, " = ", n, "_nu[$1]; ",
            "dhdb_NL", reg, " = ", n, "_dhdb_NL[$1]; "];
        ElseIf(material~{i} == 4) // infinite regions
          str = StrCat["mu", reg, " = mu0; ", "nu", reg, " = 1/mu0; "];
        EndIf
        Parse[str];
        If(export && StrLen[str])
          Printf(Str[str]) >> Str[exportFile];
        EndIf
        Parse[str2];
        If(export && StrLen[str2])
          Printf(Str[str2]) >> Str[exportFile];
        EndIf
      EndIf
    EndFor
    If(export)
      Printf('}') >> Str[exportFile];
    EndIf
  EndIf

  // other constant parameters needed by the model
  DefineConstant[
    Val_Rint = {1, Visible NbrRegions[Domain_Inf],
      Name "Parameters/Geometry/1Internal shell radius"},
    Val_Rext = {2, Visible NbrRegions[Domain_Inf],
      Name "Parameters/Geometry/2External shell radius"},
    Val_Cx, Val_Cy, Val_Cz,
    Nb_max_iter = {30, Visible NbrRegions[Domain_NL],
      Name "Parameters/Nonlinear solver/Maximum number of iterations"},
    relaxation_factor = 1,
    stop_criterion = {1e-5, Visible NbrRegions[Domain_NL],
      Name "Parameters/Nonlinear solver/Tolerance"}
  ];
}

Jacobian {
  { Name JVol;
    Case {
      { Region Domain_Inf;
        Jacobian VolSphShell{Val_Rint, Val_Rext, Val_Cx, Val_Cy, Val_Cz}; }
      { Region All; Jacobian Vol; }
    }
  }
}

Integration {
  { Name I1;
    Case {
      { Type Gauss;
        Case {
          { GeoElement Point; NumberOfPoints  1; }
          { GeoElement Line; NumberOfPoints  3; }
          { GeoElement Triangle; NumberOfPoints  3; }
          { GeoElement Quadrangle; NumberOfPoints  4; }
          { GeoElement Tetrahedron; NumberOfPoints  4; }
          { GeoElement Hexahedron; NumberOfPoints  6; }
          { GeoElement Prism; NumberOfPoints  9; }
          { GeoElement Pyramid; NumberOfPoints  8; }
	}
      }
    }
  }
}

If(interactive)
  constraintNames() = Str["phi", "a"];
  constraintNum() = {1, 1};
  For j In {0:#constraintNames()-1}
    str = StrCat["Constraint { { Name ", constraintNames(j), "; Case { "];
    For i In {1:numPhysicals}
      If(dim~{i} < modelDim)
        If(bc~{i} == constraintNum(j))
          str = StrCat[str, Sprintf["{ Region Region[%g]; Value %g; } ",
              tag~{i}, bc_val~{i}]];
        EndIf
      EndIf
    EndFor
    str = StrCat[str, "} } }"];
    Parse[str];
    If(export)
      Printf(Str[str]) >> Str[exportFile];
    EndIf
  EndFor
  If(export)
    Printf('Include "Magnetostatics.pro";') >> Str[exportFile];
  EndIf
EndIf

Constraint {
  { Name GaugeCondition_a ; Type Assign ;
    Case {
      { Region Domain ; SubRegion Domain_Dirichlet ; Value 0. ; }
    }
  }
}

FunctionSpace {
  { Name Hgrad_phi; Type Form0;
    BasisFunction {
      { Name sn; NameOfCoef phin; Function BF_Node;
        Support Domain; Entity NodesOf[ All ]; }
    }
    Constraint {
      { NameOfCoef phin; EntityType NodesOf; NameOfConstraint phi; }
    }
  }
  If(modelDim == 3)
    { Name Hcurl_a; Type Form1;
      BasisFunction {
        { Name se; NameOfCoef ae; Function BF_Edge; Support Domain ;
          Entity EdgesOf[ All ]; }
      }
      Constraint {
        { NameOfCoef ae;  EntityType EdgesOf; NameOfConstraint a; }
        { NameOfCoef ae;  EntityType EdgesOfTreeIn; EntitySubType StartingOn;
          NameOfConstraint GaugeCondition_a ; }
      }
    }
  Else
    { Name Hcurl_a; Type Form1P;
      BasisFunction {
        { Name se; NameOfCoef ae; Function BF_PerpendicularEdge;
          Support Domain; Entity NodesOf[ All ]; }
      }
      Constraint {
        { NameOfCoef ae; EntityType NodesOf; NameOfConstraint a; }
      }
    }
  EndIf
}

Formulation {
  { Name MagSta_phi; Type FemEquation;
    Quantity {
      { Name phi; Type Local; NameOfSpace Hgrad_phi; }
    }
    Equation {
      Galerkin { [ - mu[-{d phi}] * Dof{d phi} , {d phi} ];
        In Domain; Jacobian JVol; Integration I1; }
      Galerkin { JacNL [ - dbdh_NL[-{d phi}] * Dof{d phi} , {d phi} ];
        In Domain_NL; Jacobian JVol; Integration I1; }
      Galerkin { [ - mu[] * hc[] , {d phi} ];
        In Domain_M; Jacobian JVol; Integration I1; }
    }
  }
  { Name MagSta_a; Type FemEquation;
    Quantity {
      { Name a; Type Local; NameOfSpace Hcurl_a; }
    }
    Equation {
      Galerkin { [ nu[{d a}] * Dof{d a} , {d a} ];
        In Domain; Jacobian JVol; Integration I1; }
      Galerkin { JacNL [ dhdb_NL[{d a}] * Dof{d a} , {d a} ];
        In Domain_NL; Jacobian JVol; Integration I1; }
      Galerkin { [ hc[] , {d a} ];
        In Domain_M; Jacobian JVol; Integration I1; }
      Galerkin { [ -js[] , {a} ];
        In Domain_S; Jacobian JVol; Integration I1; }
    }
  }
}

Resolution {
  { Name MagSta_phi;
    System {
      { Name A; NameOfFormulation MagSta_phi; }
    }
    Operation {
      CreateDir[resPath];
      If(!NbrRegions[Domain_NL])
        Generate[A]; Solve[A];
      Else
        IterativeLoop[Nb_max_iter, stop_criterion, relaxation_factor]{
          GenerateJac[A]; SolveJac[A];
        }
      EndIf
      SaveSolution[A];
    }
  }
  { Name MagSta_a;
    System {
      { Name A; NameOfFormulation MagSta_a; }
    }
    Operation {
      CreateDir[resPath];
      If(!NbrRegions[Domain_NL])
        Generate[A]; Solve[A];
      Else
        IterativeLoop[Nb_max_iter, stop_criterion, relaxation_factor]{
          GenerateJac[A]; SolveJac[A];
        }
      EndIf
      SaveSolution[A];
    }
  }
  { Name Analysis;
    System {
      If(formulationType == 0)
        { Name A; NameOfFormulation MagSta_phi; }
      Else
        { Name A; NameOfFormulation MagSta_a; }
      EndIf
    }
    Operation {
      CreateDir[resPath];
      If(!NbrRegions[Domain_NL])
        Generate[A]; Solve[A];
      Else
        //IterativeLoopN[ Nb_max_iter, relaxation_factor,
        //                System { {A, reltol, abstol, Solution MeanL2Norm} } ]{
        IterativeLoop[Nb_max_iter, stop_criterion, relaxation_factor]{
          GenerateJac[A]; SolveJac[A];
        }
      EndIf
      SaveSolution[A];
      If(formulationType == 0)
        PostOperation[MagSta_phi];
      Else
        PostOperation[MagSta_a];
      EndIf
    }
  }
}

PostProcessing {
  { Name MagSta_phi; NameOfFormulation MagSta_phi;
    Quantity {
      { Name b; Value { Local { [ - mu[-{d phi}] * {d phi} ]; In Domain; Jacobian JVol; }
                        Local { [ - mu[] * hc[] ]; In Domain_M; Jacobian JVol; } } }
      { Name h; Value { Local { [ - {d phi} ]; In Domain; Jacobian JVol; } } }
      { Name hc; Value { Local { [ hc[] ]; In Domain_M; Jacobian JVol; } } }
      { Name phi; Value { Local { [ {phi} ]; In Domain; Jacobian JVol; } } }
    }
  }
  { Name MagSta_a; NameOfFormulation MagSta_a;
    Quantity {
      { Name az; Value { Local { [ CompZ[{a}] ]; In Domain; Jacobian JVol; } } }
      { Name b; Value { Local { [ {d a} ]; In Domain; Jacobian JVol; } } }
      { Name a; Value { Local { [ {a} ]; In Domain; Jacobian JVol; } } }
      { Name h; Value { Local { [ nu[{d a}] * {d a} ]; In Domain; Jacobian JVol; }
                        Local { [ hc[] ]; In Domain_M; Jacobian JVol; } } }
      { Name hc; Value { Local { [ hc[] ]; In Domain_M; Jacobian JVol; } } }
      { Name js; Value { Local { [ js[] ]; In Domain_S; Jacobian JVol; } } }
    }
  }
}

PostOperation {
  { Name MagSta_phi; NameOfPostProcessing MagSta_phi;
    Operation {
      Print[ hc, OnElementsOf Domain_M, File StrCat[resPath, "MagSta_phi_hc.pos"] ];
      Print[ phi, OnElementsOf Domain, File StrCat[resPath, "MagSta_phi_phi.pos"] ];
      Print[ h, OnElementsOf Domain, File StrCat[resPath, "MagSta_phi_h.pos"] ];
      Print[ b, OnElementsOf Domain, File StrCat[resPath, "MagSta_phi_b.pos"] ];
    }
  }
  { Name MagSta_a; NameOfPostProcessing MagSta_a;
    Operation {
      Print[ hc, OnElementsOf Domain_M, File StrCat[resPath, "MagSta_a_hc.pos"] ];
      Print[ js, OnElementsOf Domain_S, File StrCat[resPath, "MagSta_a_js.pos"] ];
      If(modelDim == 2)
        Print[ az, OnElementsOf Domain, File StrCat[resPath, "MagSta_a_az.pos"] ];
      EndIf
      Print[ h, OnElementsOf Domain, File StrCat[resPath, "MagSta_a_h.pos"] ];
      Print[ b, OnElementsOf Domain, File StrCat[resPath, "MagSta_a_b.pos"] ];
    }
  }
}

DefineConstant[
  R_ = {"Analysis", Name "GetDP/1ResolutionChoices", Visible 0},
  C_ = {"-solve -v2", Name "GetDP/9ComputeCommand", Visible 0},
  P_ = {"", Name "GetDP/2PostOperationChoices", Visible 0}
];
