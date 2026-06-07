import json

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from io import BytesIO
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from apps.productos.models import Producto, Categoria
from apps.productores.models import Productor


def reportes(request):

    categorias = Categoria.objects.annotate(
        total_productos=Count('productos')
    ).order_by('nombre')

    municipios = Productor.objects.values(
        'municipio'
    ).annotate(
        total_productores=Count('id')
    ).order_by('municipio')

    productos_por_categoria = Categoria.objects.annotate(
        total=Count('productos')
    ).values('nombre', 'total')

    productores_por_municipio = Productor.objects.values(
        'municipio'
    ).annotate(
        total=Count('id')
    ).order_by('municipio').values('municipio', 'total')

    categorias_labels = [
        item["nombre"]
        for item in productos_por_categoria
    ]
    categorias_data = [
        item["total"]
        for item in productos_por_categoria
    ]

    municipios_labels = [
        item["municipio"]
        for item in productores_por_municipio
    ]
    municipios_data = [
        item["total"]
        for item in productores_por_municipio
    ]

    total_productos = Producto.objects.count()
    total_productores = Productor.objects.count()
    total_categorias = Categoria.objects.count()
    productos_activos = Producto.objects.filter(
        activo=True
    ).count()

    return render(
        request,
        'reportes/reportes.html',
        {
            'categorias': categorias,
            'municipios': municipios,
            'total_productos': total_productos,
            'total_productores': total_productores,
            'total_categorias': total_categorias,
            'productos_activos': productos_activos,
            'categorias_labels': categorias_labels,
            'categorias_data': categorias_data,
            'municipios_labels': municipios_labels,
            'municipios_data': municipios_data,
            'categorias_labels_json': json.dumps(categorias_labels),
            'categorias_data_json': json.dumps(categorias_data),
            'municipios_labels_json': json.dumps(municipios_labels),
            'municipios_data_json': json.dumps(municipios_data),
        },
    )


def exportar_productos_excel(request):

    wb = Workbook()

    ws = wb.active
    ws.title = "Productos"

    ws.append([
        "Nombre",
        "Categoria",
        "Activo"
    ])

    productos = Producto.objects.all()

    for producto in productos:
        ws.append([
            producto.nombre,
            str(producto.categoria),
            "Si" if producto.activo else "No"
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=productos.xlsx'

    wb.save(response)

    return response


def exportar_productores_excel(request):

    wb = Workbook()

    ws = wb.active
    ws.title = "Productores"

    ws.append([
        "Nombre",
        "Municipio",
        "Telefono"
    ])

    productores = Productor.objects.all()

    for productor in productores:

        ws.append([
            productor.nombre_comercial,
            productor.municipio,
            productor.telefono
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=productores.xlsx'

    wb.save(response)

    return response


def exportar_pdf(request):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "MASXMENOS — Reporte del Marketplace",
            styles['Title'],
        )
    )
    elements.append(Spacer(1, 12))
    elements.append(
        Paragraph(
            f"Fecha: {timezone.now().strftime('%d/%m/%Y %H:%M')}",
            styles['Normal'],
        )
    )
    elements.append(Spacer(1, 20))

    total_productos = Producto.objects.count()
    total_productores = Productor.objects.count()
    total_categorias = Categoria.objects.count()
    productos_activos = Producto.objects.filter(activo=True).count()

    elements.append(
        Paragraph("Resumen general", styles['Heading2'])
    )
    elements.append(Spacer(1, 8))

    resumen_data = [
        ["Indicador", "Valor"],
        ["Total productos", str(total_productos)],
        ["Total productores", str(total_productores)],
        ["Total categorías", str(total_categorias)],
        ["Productos activos", str(productos_activos)],
    ]

    resumen_table = Table(resumen_data, colWidths=[200, 100])
    resumen_table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ])
    )
    elements.append(resumen_table)
    elements.append(Spacer(1, 24))

    categorias = Categoria.objects.annotate(
        total_productos=Count('productos')
    ).order_by('nombre')

    elements.append(
        Paragraph("Productos por categoría", styles['Heading2'])
    )
    elements.append(Spacer(1, 8))

    categorias_data = [["Categoría", "Cantidad"]]
    for categoria in categorias:
        categorias_data.append([
            categoria.nombre,
            str(categoria.total_productos),
        ])

    if len(categorias_data) == 1:
        categorias_data.append(["Sin categorías registradas", "0"])

    categorias_table = Table(categorias_data, colWidths=[200, 100])
    categorias_table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ])
    )
    elements.append(categorias_table)

    doc.build(elements)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte_masxmenos.pdf'
    response.write(buffer.getvalue())
    buffer.close()

    return response
