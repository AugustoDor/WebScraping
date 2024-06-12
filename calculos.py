#costo compra total es el total por el cual de efectua la compra del inmueble
def costo_compra_total(costo_compra, costo_reformas, porcentaje_agencia, costo_tramites, porcentaje_impuesto):
    comision_agencia = costo_compra * porcentaje_agencia
    impuesto = costo_compra * porcentaje_impuesto
    total = costo_compra + costo_reformas + costo_tramites + comision_agencia + impuesto
    return total


#monto a pagar es el total que estamos pagando nosotros de nuestro bolsillo y cuando paga el banco
def monto_pagar(costo_compra):
    hipoteca = costo_compra * 0.8
    dinero = costo_compra * 0.2
    return hipoteca, dinero


#ingreso bruto es el total ganado con el alquiler sin tener en cuenta gastos
def ingreso_bruto_alquiler(costo_compra, ingreso_bruto_mensual):
    ingreso_bruto_anual = ingreso_bruto_mensual * 12
    rentabilidad_bruta = (ingreso_bruto_anual * 100) / costo_compra
    return ingreso_bruto_mensual, ingreso_bruto_anual, rentabilidad_bruta


#ingreso neto antes de impuesto es el total ganado con el alquiler teniendo en cuenta los gastos pero no los impuestos
def ingreso_neto_alquiler(ingresos_brutos, costo_compra, total_pagar_mensual):
    ingresos_netos = ingresos_brutos - total_pagar_mensual
    rentabilidad_neta = (ingresos_netos * 100) / costo_compra
    return ingresos_netos, rentabilidad_neta


#ingreso neto despues de impuesto es el ingreso neto ai pero ahora teniendo en cuenta los impuestos
def ingreso_neto_alquiler_despues_impuesto(ingreso_neto, impuestos):
    return ingreso_neto - impuestos


#cashflow es
def cashflow(ingreso_neto_despues_impuesto, hipoteca):
    return ingreso_neto_despues_impuesto - hipoteca


#roce es
def roce(cashflow, total_pagado):
    return (cashflow / total_pagado) * 100