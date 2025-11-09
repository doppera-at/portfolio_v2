<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">

<html>
<body>
    <h2>List of basic Kanji</h2>

    <table>
        <tr>
            <th>Kanji</th>
            <th>Meaning</th>
        </tr>

        <xsl:for-each select="kanji-list/kanji">
        <tr>
            <td><xsl:value-of select="character"/></td>
            <td><xsl:value-of select="meaning"/></td>
        </tr>
        </xsl:for-each>
    </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>