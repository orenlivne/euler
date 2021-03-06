drop table if exists %TABLE_NAME%;

create table %TABLE_NAME%
(
  record_id INT AUTO_INCREMENT PRIMARY KEY,
  vtools_id INT,
  chrom CHAR(2),
  pos INT,
  ref VARCHAR(30),
  alt VARCHAR(30),
  dbSNP_name VARCHAR(30),
  dbSNP_class VARCHAR(30),
  dbSNP_func VARCHAR(30),
  region_type VARCHAR(30),
  mut_type VARCHAR(30),
  evs_6500_AminoAcidChange VARCHAR(30),
  refGene2 VARCHAR(30),
  ccdsGene VARCHAR(30),
  evs_6500_EuropeanAmericanMaf VARCHAR(30),
  evs_6500_AfricanAmericanMaf VARCHAR(30),
  thousandGenomesEBI_AMR_AF_INFO VARCHAR(30),
  thousandGenomesEBI_ASN_AF_INFO VARCHAR(30),
  thousandGenomesEBI_AFR_AF_INFO VARCHAR(30),
  thousandGenomesEBI_EUR_AF_INFO VARCHAR(30),
  ANNOVAR_maf_ALL VARCHAR(30),
  ANNOVAR_maf_AMR VARCHAR(30),
  ANNOVAR_maf_AFR VARCHAR(30),
  ANNOVAR_maf_ASN VARCHAR(30),
  ANNOVAR_maf_EUR VARCHAR(30),
  LRT_score VARCHAR(30),
  PhyloP_score VARCHAR(30),
  SIFT_score VARCHAR(30),
  MutationTaster_score VARCHAR(30),
  GERP_RS VARCHAR(30),
  Polyphen2_HDIV_score VARCHAR(30),
  regulation_NHLF VARCHAR(30),
  regulation_HMECregulation_NHEK VARCHAR(30),
  regulation_GM12878 VARCHAR(30),
  regulomeDB VARCHAR(30),
  INDEX name (chrom, pos),
  INDEX region (region_type)
);

# Load all columns from file except record_id, which will automatically be generated by MySQL upon loading.
LOAD DATA LOCAL INFILE '%IN_FILE%' INTO TABLE %TABLE_NAME% (vtools_id,chrom,pos,ref,alt,dbSNP_name,dbSNP_class,dbSNP_func,region_type,mut_type,evs_6500_AminoAcidChange,refGene2,ccdsGene,evs_6500_EuropeanAmericanMaf,evs_6500_AfricanAmericanMaf,thousandGenomesEBI_AMR_AF_INFO,thousandGenomesEBI_ASN_AF_INFO,thousandGenomesEBI_AFR_AF_INFO,thousandGenomesEBI_EUR_AF_INFO,ANNOVAR_maf_ALL,ANNOVAR_maf_AMR,ANNOVAR_maf_AFR,ANNOVAR_maf_ASN,ANNOVAR_maf_EUR,LRT_score,PhyloP_score,SIFT_score,MutationTaster_score,GERP_RS,Polyphen2_HDIV_score,regulation_NHLF,regulation_HMECregulation_NHEK,regulation_GM12878,regulomeDB);
