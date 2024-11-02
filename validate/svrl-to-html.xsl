<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cml="http://www.xml-cml.org/schema" xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
  xmlns="http://www.w3.org/1999/xhtml" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:gvr="http://validationreport.gazelle.ihe.net/" version="2.0">
<xsl:param name="elapsedTime" />
<xsl:param name="title" />
<xsl:param name="nameFile" />
  <xsl:template match="/">
    <xsl:apply-templates />
  </xsl:template>


  <xsl:template match="gvr:validationReport ">

  
  <div class="accordion-item">
    <h2 class="accordion-header">
    <xsl:choose>
      <xsl:when test="@result='PASSED'">
        <button class="accordion-button collapsed" style="background-color:#438552;color:white" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapsexxxxx" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
        <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validationServiceName" />-<xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validatorID" /> : <xsl:value-of select="@result" />
        <br/>Nombre d'erreurs : <xsl:value-of select="//gvr:counters/@numberOfErrors" />
        <br/>Nombre de warnings :  <xsl:value-of select="//gvr:counters/@numberOfWarnings" />
        <br/>Temps d'execution :  <xsl:value-of select="$elapsedTime"/>
        <br/>Nombre de règles:  <xsl:value-of select="//gvr:counters/@numberOfConstraints"/>
        </button>
      </xsl:when>
       <xsl:otherwise>
        <button class="accordion-button collapsed" style="background-color:#894f55;color:white" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapsexxxxx" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
        <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validationServiceName" />-<xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validatorID" /> : <xsl:value-of select="@result" />
        <br/>Nombre d'erreurs : <xsl:value-of select="//gvr:counters/@numberOfErrors" />
        <br/>Nombre de warnings :  <xsl:value-of select="//gvr:counters/@numberOfWarnings" />
        <br/>Temps d'execution :  <xsl:value-of select="$elapsedTime"/>
        <br/>Nombre de règles:  <xsl:value-of select="//gvr:counters/@numberOfConstraints"/>
        </button>




      </xsl:otherwise>
    </xsl:choose>  

    </h2>
    <div id="panelsStayOpen-collapsexxxxx" class="accordion-collapse collapse ">
      <div class="accordion-body">
   <table class="table table-striped table-hover">
  <thead>
    <tr>
      <th scope="col">Validation</th>
      <th scope="col" style="width: 50%">résulat</th>
    </tr>
  </thead>
  <tbody>
		<xsl:apply-templates />
		
  </tbody>
</table>		
     </div>
    </div>
  </div>



  </xsl:template>

  <xsl:template match="gvr:subReport">
  

    <tr>
      <td>	  
		   <xsl:value-of select="@name" />
	</td>
      <td class=".small">
	  <xsl:value-of select="@subReportResult" />
    <table class="table table-striped table-hover">
     <xsl:apply-templates />
     </table>
    </td>
     
    </tr>
    


  </xsl:template>

    <xsl:template match="gvr:constraint">
	
    <tr>
      <td>	  
		  <xsl:value-of select="@severity" />
	</td>
      <td class=".small"><small>
      <xsl:value-of select="gvr:constraintDescription" />
       <br/>
      <xsl:value-of select="gvr:locationInValidatedObject" />
      </small></td>

    </tr>
	

  

       
    </xsl:template>

  <xsl:template match="*">
    <!-- drop these -->
  </xsl:template>
  
<xsl:template name="break">
  <xsl:param name="text" select="string(.)"/>
  <xsl:choose>
    <xsl:when test="contains($text, '&#xa;')">
      <xsl:value-of select="substring-before($text, '&#xa;')"/>
      <br/>
      <xsl:call-template name="break">
        <xsl:with-param 
          name="text" 
          select="substring-after($text, '&#xa;')"
        />
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$text"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>  
  
</xsl:stylesheet>
